<template>
  <div class="min-h-screen bg-gray-100 flex flex-col md:flex-row">
    <!-- Sidebar / Navigation -->
    <aside class="w-full md:w-64 bg-slate-900 text-gray-300 flex-shrink-0 border-r border-slate-800">
      <!-- App Header / Logo -->
      <div class="h-16 flex items-center px-6 bg-slate-950 font-bold text-white tracking-wide text-lg border-b border-slate-800">
        <span class="text-indigo-500 mr-2">⚡</span> Logistics Portal
      </div>

      <!-- Nav Links -->
      <nav class="p-4 space-y-1">
        <RouterLink 
          to="/" 
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors hover:bg-slate-800 hover:text-white"
          active-class="bg-indigo-600 text-white hover:bg-indigo-700"
        >
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 00-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 00-1 1m-6 0h6" />
          </svg>
          Dashboard
        </RouterLink>

        <RouterLink 
          to="/shipments" 
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors hover:bg-slate-800 hover:text-white"
          active-class="bg-indigo-600 text-white hover:bg-indigo-700"
        >
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
          Shipments
        </RouterLink>
        <RouterLink 
          to="/addshipment" 
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors hover:bg-slate-800 hover:text-white"
          active-class="bg-indigo-600 text-white hover:bg-indigo-700"
        >
          Add Shipment
        </RouterLink>
      </nav>
    </aside>

    <!-- Main Content Canvas -->
    <main class="flex-1 min-w-0 overflow-y-auto">
      <div class="py-6">
        <RouterView />
      </div>
    </main>
  </div>
</template>