<script lang="ts">
	import * as XLSX from 'xlsx';
	import type { DeploymentDetails } from '../../../models/classes/deployment-details.model';
  
    let file: File;
    export let deploymentDetails: DeploymentDetails[] = [];
  
    function handleFileUpload(e: Event) {
      file = (e.target as HTMLInputElement).files[0];
      const reader = new FileReader();
  
      reader.onload = (event) => {
        const data = new Uint8Array(event.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
  
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
  
        const jsonData = XLSX.utils.sheet_to_json<DeploymentDetails>(worksheet);
  
        deploymentDetails = jsonData;
      };
  
      reader.readAsArrayBuffer(file);
    }
  </script>
  
  <div class="w-full">
    <input
      type="file"
      id="file-upload"
      on:change={handleFileUpload}
      class="hidden"
      accept=".xlsx, .xls"
    />
    <label
      for="file-upload"
      class="cursor-pointer px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-blue-800"
    >
      Upload Excel File
    </label>
  </div>
  