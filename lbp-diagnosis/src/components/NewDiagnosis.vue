<template>
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold">New Diagnosis Session</h2>
    <v-btn small @click="onClickBackButton" prepend-icon="mdi-arrow-left"
      class="!bg-secondary !text-pink-200">Back</v-btn>

    <!-- hidden inputs -->
    <input ref="singleTextFileInput" type="file" accept=".txt" hidden @change="onSingleTextFileSelected" />
    <input ref="singleImageFileInput" type="file" accept="image/*" hidden @change="onSingleImageFileSelected" />
    <input ref="zipFileInput" type="file" accept=".zip" hidden @change="onZipFileSelected" />

    <!-- Table -->
    <v-data-table :headers="headers" :items="paginatedEntries" :items-per-page="itemsPerPage"
      class="elevation-1 !bg-white" hide-default-footer>
      <!-- Custom header -->
      <template #headers="{ columns }">
        <tr>
          <th v-for="col in columns" :key="col.key ?? col.title"
            class="px-4 py-2 text-base !font-bold text-black bg-sky-200">
            {{ col.title }}
          </th>
        </tr>
      </template>

      <!-- Custom rows -->
      <template #item="{ item, index }">
        <tr class="border-b border-gray-300">
          <!-- Image column -->
          <td class="px-4 py-2">
            <div class="flex items-center gap-2">
              <v-btn small @click="openImageDialog((page - 1) * itemsPerPage + index)" class="!bg-primary !text-white"
                prepend-icon="mdi-upload">
                Upload Image
              </v-btn>
              <span v-if="item.image">{{ item.image.name }}</span>
            </div>
          </td>

          <!-- Text column -->
          <td class="px-4 py-2">
            <div class="flex items-center gap-2">
              <v-btn small @click="openTextFileDialog((page - 1) * itemsPerPage + index)"
                class="!bg-primary !text-white" prepend-icon="mdi-upload">
                Upload Text
              </v-btn>

              <v-btn small @click="editText((page - 1) * itemsPerPage + index)" class="!bg-cyan-300"
                prepend-icon="mdi-pencil">
                Edit
              </v-btn>

              <span class="truncate max-w-[200px]">{{ item.text }}</span>
            </div>
          </td>

          <!-- Actions column -->
          <td class="px-4 py-2">
            <v-btn small @click="removeEntry((page - 1) * itemsPerPage + index)" class="!bg-error !text-white"
              prepend-icon="mdi-delete">
              Delete
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>

    <!-- Pagination -->
    <div class="flex justify-center mt-4">
      <v-pagination v-model="page" :length="Math.ceil(entries.length / itemsPerPage)" :total-visible="7"
        show-first-last-page class="bg-white rounded-2xl" />
    </div>


    <!-- Action buttons -->
    <div class="flex gap-2 mt-4 flex-wrap">
      <v-btn prepend-icon="mdi-plus" @click="addEntry" class="!bg-cyan-300" :disabled="isLoading">Add Pair</v-btn>

      <v-btn prepend-icon="mdi-folder-zip" @click="openZipDialog" class="!bg-cyan-300" :disabled="isLoading">Upload
        ZIP</v-btn>

      <v-btn @click="submit" prepend-icon="mdi-play" class="!bg-cyan-300" :disabled="isLoading">
        <v-progress-circular v-if="isLoading" indeterminate size="20" width="2" class="mr-2"></v-progress-circular>
        <span v-if="!isLoading">Run Session</span>
        <span v-else>Running...</span>
      </v-btn>
    </div>

    <!-- Dialog for editing text -->
    <v-dialog v-model="dialogText" max-width="600">
      <v-card class="!bg-white">
        <v-card-title>Edit Diagnosis Text</v-card-title>
        <v-card-text>
          <v-textarea v-model="editingText" auto-grow outlined />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialogText = false" class="!bg-gray-300">Cancel</v-btn>
          <v-btn text @click="saveText" class="!bg-primary">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

  <!-- Dialog for ZIP upload -->
  <v-dialog v-model="dialogZip" max-width="600">
    <v-card class="!bg-white">
      <v-card-title class="text-xl font-bold">Upload ZIP File</v-card-title>
      <v-card-text>
        <p class="mb-4">
          Please structure your ZIP file like this:
        </p>
        <ul class="list-disc ml-6 mb-4">
          <li>Each case in its own folder</li>
          <li>One <b>.jpg/.png</b> file per case</li>
          <li>One <b>.txt</b> file per case (same folder)</li>
        </ul>

        <v-btn prepend-icon="mdi-folder-zip" class="!bg-primary !text-white" @click="triggerZipInput">
          Select ZIP
        </v-btn>
        <input ref="zipFileInput" type="file" accept=".zip" hidden @change="onZipFileSelected" />

        <div v-if="selectedZipName" class="mt-2 text-gray-600">
          Selected: {{ selectedZipName }}
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialogZip = false" class="!bg-gray-300">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script setup lang="ts">
import { ref, type Ref, computed } from "vue"
import { useRouter } from "vue-router"
import JSZip from "jszip"

import { useSessionViewStore } from '../stores/sessionViewStore'
import { useToastStore } from '../stores/toastStore'
import { useDiagnosisSessionStore } from '../stores/diagnosisSessionStore'

import { runDiagnosisSession } from '../api/diagnosis_api'

const router = useRouter()

const sessionViewStore = useSessionViewStore()
const toastStore = useToastStore()
const diagnosisStore = useDiagnosisSessionStore()

interface Entry {
  image: File | null
  text: string
  fileName?: string
}

const headers = [
  { title: "Image", value: "image" },
  { title: "Diagnosis Text", value: "text" },
  { title: "Actions", value: "actions", sortable: false },
]

const entries = ref<Entry[]>([{ image: null, text: "" }])

// hidden input refs
const singleTextFileInput: Ref<HTMLInputElement | null> = ref(null)
const singleImageFileInput: Ref<HTMLInputElement | null> = ref(null)
const zipFileInput: Ref<HTMLInputElement | null> = ref(null)

// active index for upload
const activeTextIndex = ref<number | null>(null)
const activeImageIndex = ref<number | null>(null)

// pagination
const page = ref(1)
const itemsPerPage = 5
const isLoading = ref(false)

// dialog for text editing
const dialogText = ref(false)
const editingIndex = ref<number | null>(null)
const editingText = ref("")
const dialogZip = ref(false)
const selectedZipName = ref("")

const paginatedEntries = computed(() => {
  const start = (page.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return entries.value.slice(start, end)
})

function onClickBackButton() {
  sessionViewStore.setNewDiagnosis(false)
}

function addEntry() {
  entries.value.push({ image: null, text: "" })
}
function removeEntry(index: number) {
  entries.value.splice(index, 1)
}

// IMAGE UPLOAD
function openImageDialog(index: number) {
  activeImageIndex.value = index
  singleImageFileInput.value?.click()
}
function onSingleImageFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  const i = activeImageIndex.value
  if (!file || i === null) return

  entries.value[i].image = file
  if (singleImageFileInput.value) singleImageFileInput.value.value = ""
  activeImageIndex.value = null
}

// TEXT UPLOAD
function openTextFileDialog(index: number) {
  activeTextIndex.value = index
  singleTextFileInput.value?.click()
}
function onSingleTextFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  const i = activeTextIndex.value
  if (!file || i === null) return

  entries.value[i].fileName = file.name
  const reader = new FileReader()
  reader.onload = () => (entries.value[i].text = String(reader.result ?? ""))
  reader.readAsText(file)

  if (singleTextFileInput.value) singleTextFileInput.value.value = ""
  activeTextIndex.value = null
}

// TEXT EDITING
function editText(index: number) {
  editingIndex.value = index
  editingText.value = entries.value[index].text
  dialogText.value = true
}
function saveText() {
  if (editingIndex.value !== null) {
    entries.value[editingIndex.value].text = editingText.value
  }
  dialogText.value = false
}

function openZipDialog() {
  dialogZip.value = true
}

function triggerZipInput() {
  zipFileInput.value?.click()
}

async function onZipFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  selectedZipName.value = file.name

  const zip = new JSZip()
  const contents = await zip.loadAsync(file)

  // Organize files by folder
  const folderMap: Record<string, { images: File[]; texts: string[]; textFiles: string[] }> = {}

  for (const [relativePath, zipEntry] of Object.entries(contents.files)) {
    if (zipEntry.dir) continue // skip folders
    const parts = relativePath.split("/")
    if (parts.length < 2) {
      toastStore.error(`Invalid file placement: "${relativePath}".`)
      return
    }

    const folder = parts[0]
    if (!folderMap[folder]) {
      folderMap[folder] = { images: [], texts: [], textFiles: [] }
    }

    if (/\.(jpg|jpeg|png)$/i.test(relativePath)) {
      const blob = await zipEntry.async("blob")
      const imageFile = new File([blob], parts[parts.length - 1], { type: "image/png" })
      folderMap[folder].images.push(imageFile)
    } else if (relativePath.endsWith(".txt")) {
      const text = await zipEntry.async("text")
      folderMap[folder].texts.push(text)
      folderMap[folder].textFiles.push(parts[parts.length - 1])
    } else {
      toastStore.error(`Unsupported file type: "${relativePath}"`)
      return
    }
  }

  // Validate folder contents
  for (const [folder, { images, texts }] of Object.entries(folderMap)) {
    if (images.length !== 1 || texts.length !== 1) {
      toastStore.error(
        `Folder "${folder}" must contain exactly 1 image and 1 text file. Found ${images.length} image(s), ${texts.length} text(s).`
      )
      return
    }
  }

  // If valid, build entries
  const newEntries: Entry[] = []
  for (const [folder, { images, texts, textFiles }] of Object.entries(folderMap)) {
    newEntries.push({
      image: images[0],
      text: texts[0],
      fileName: `${folder}/${textFiles[0]}`
    })
  }

  entries.value = newEntries
  dialogZip.value = false
  if (zipFileInput.value) zipFileInput.value.value = ""
  toastStore.success("ZIP imported successfully!")
}


// SUBMIT
async function submit() {
  if (!entries.value.length) {
    toastStore.error("Please add at least one entry before submitting")
    return
  }

  const formData = new FormData()
  entries.value.forEach(entry => {
    if (entry.image) formData.append("files", entry.image)
    formData.append("texts", entry.text)
  })

  try {
    isLoading.value = true
    const res = await runDiagnosisSession(formData)
    toastStore.success("Diagnosis session created successfully!")

    // 🔥 Optionally refresh the sessions list immediately
    await diagnosisStore.fetchSessions()

    router.push({
      name: "Diagnosis",
      query: { sessionId: res.session_id }
    })

    // 🔥 Or redirect to the session detail
    // router.push({ name: "Diagnosis", query: { sessionId: res.session_id } })

  } catch (err: any) {
    toastStore.error(err.response?.data?.detail || "Failed to create session")
  } finally {
    isLoading.value = false
  }
}
</script>
