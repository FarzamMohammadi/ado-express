<script lang="ts">
  import { saveAs } from 'file-saver';
  import * as XLSX from 'xlsx';
  import type { IDeploymentDetails } from '../../../models/interfaces/ideployment-details.interface';
  import { runResultData } from '../../../utils/stores';

  export let matrixTheme: boolean;
  let buttonClass: string;
  let hasValidDeploymentDetails: boolean;

  function downloadResultsAsExcelFile(): void {
    let updatedData = [];

    if (hasValidDeploymentDetails) {
      const deploymentDetails = $runResultData as IDeploymentDetails;
      const deploymentDetailsArray = Object.values(deploymentDetails);

      updatedData = deploymentDetailsArray.map((item) => ({
        'Project Name': item.releaseProjectName,
        'Release Name': item.releaseName,
        'Release Number': item.releaseNumber,
        'Rollback Number': item.releaseRollback,
        'Is Crucial': item.isCrucial,
      }));
    }

    const ws = XLSX.utils.json_to_sheet(updatedData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([wbout], { type: 'application/octet-stream' });
    saveAs(blob, 'results.xlsx');
  }

  $: if (matrixTheme) {
    buttonClass =
      'focus:ring-1 focus:outline-none focus:ring-green-500 bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-green-800 hover:border-transparent rounded-lg shadow-lg';
  } else {
    buttonClass =
      'focus:ring-1 focus:outline-none focus:ring-purple-500 bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-purple-800 hover:border-transparent rounded-lg shadow-lg';
  }

  $: hasValidDeploymentDetails = $runResultData !== undefined && Object.values($runResultData)[0].releaseProjectName !== undefined;
</script>

<button class={buttonClass} disabled={!hasValidDeploymentDetails} on:click={downloadResultsAsExcelFile}> Download Excel </button>

<style>
  button {
    cursor: pointer;
    font-size: 14px;
    margin-top: 8px;
  }
</style>
