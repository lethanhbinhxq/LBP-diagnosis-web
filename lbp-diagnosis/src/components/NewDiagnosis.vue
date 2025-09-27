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
    <v-data-table :headers="headers" :items="entries" :items-per-page="5" class="elevation-1 !bg-white"
      hide-default-footer>
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
              <v-btn small @click="openImageDialog(index)" class="!bg-primary !text-white" prepend-icon="mdi-upload">
                Upload Image
              </v-btn>
              <span v-if="item.image">{{ item.image.name }}</span>
            </div>
          </td>

          <!-- Text column -->
          <td class="px-4 py-2">
            <div class="flex items-center gap-2">
              <v-btn small @click="openTextFileDialog(index)" class="!bg-primary !text-white" prepend-icon="mdi-upload">
                Upload Text
              </v-btn>

              <v-btn small @click="editText(index)" class="!bg-cyan-300" prepend-icon="mdi-pencil">
                Edit
              </v-btn>

              <span class="truncate max-w-[200px]">{{ item.text }}</span>
            </div>
          </td>

          <!-- Actions column -->
          <td class="px-4 py-2">
            <v-btn small @click="removeEntry(index)" class="!bg-error !text-white" prepend-icon="mdi-delete">
              Delete
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>

    <!-- Pagination -->
    <div class="flex justify-center mt-4">
      <v-pagination
        v-model="page"
        :length="Math.ceil(entries.length / 5)"
        :total-visible="7"
        show-first-last-page
        class="bg-white rounded-2xl"
      />
    </div>

    <!-- Action buttons -->
    <div class="flex gap-2 mt-4 flex-wrap">
      <v-btn prepend-icon="mdi-plus" @click="addEntry" class="!bg-cyan-300">Add Pair</v-btn>
      <v-btn prepend-icon="mdi-folder-zip" @click="openZipDialog" class="!bg-cyan-300">Upload ZIP</v-btn>
      <v-btn @click="submit" prepend-icon="mdi-play" class="!bg-cyan-300">Run Session</v-btn>
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
</template>

<script setup lang="ts">
import { ref, type Ref } from "vue"
import { useSessionViewStore } from '../stores/sessionViewStore'

const sessionViewStore = useSessionViewStore()

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

// dialog for text editing
const dialogText = ref(false)
const editingIndex = ref<number | null>(null)
const editingText = ref("")

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

// ZIP UPLOAD
function openZipDialog() {
  zipFileInput.value?.click()
}
function onZipFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  console.log("ZIP file selected:", file.name)
  // For now, just append it as a single entry. Normally you'd send the zip to backend for parsing
  entries.value = [{ image: null, text: `ZIP uploaded: ${file.name}`, fileName: file.name }]
  if (zipFileInput.value) zipFileInput.value.value = ""
}

// SUBMIT
async function submit() {
  const formData = new FormData()

  entries.value.forEach((entry, i) => {
    if (entry.image) formData.append(`images[${i}]`, entry.image)
    formData.append(`texts[${i}]`, entry.text)
  })

  // If a ZIP file is uploaded, you could instead send it as:
  // formData.append("zip_file", selectedZipFile)

  console.log("Submitting:", entries.value)
}
</script>
