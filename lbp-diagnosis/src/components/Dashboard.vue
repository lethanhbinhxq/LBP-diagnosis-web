<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-primary text-white p-6 space-y-4">
      <h2 class="text-xl font-bold">LBP Dashboard</h2>
      <nav class="flex flex-col gap-2">
        <RouterLink to="/dashboard/input" class="hover:bg-primary-dark px-3 py-2 rounded">
          🧠 Make Diagnosis
        </RouterLink>
        <RouterLink to="/dashboard/statistic" class="hover:bg-primary-dark px-3 py-2 rounded">
          📊 AI Model Statistics
        </RouterLink>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-6 bg-gray-50">
      <v-card title="Card title" text="..." class="!bg-primary !text-white"></v-card>
    </main>
  </div>
</template>
