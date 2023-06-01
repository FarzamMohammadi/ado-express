<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import * as XLSX from 'xlsx';

  import { DeploymentDetail } from '../../../../models/classes/deployment-detail.model';
  import { deploymentDetails } from '../../../../utils/stores';

  const dispatch = createEventDispatcher();

  function decodeBooleanValue(input: String) {
    const trueValues = ['1', 't', 'true', 'y', 'yes'];
    return trueValues.includes(input.toLowerCase());
  }

  function extractFileData(event: ProgressEvent<FileReader>) {
    const data = new Uint8Array(event.target.result as ArrayBuffer);
    const workbook = XLSX.read(data, { type: 'array' });

    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];

    const range = XLSX.utils.decode_range(worksheet['!ref']);

    const extractedData: string[][] = [];

    for (let rowNum = 1; rowNum <= range.e.r; rowNum++) {
      const rowData: string[] = [];
      for (let colNum = 0; colNum < 5; colNum++) {
        const cellAddress = XLSX.utils.encode_cell({ r: rowNum, c: colNum });
        rowData.push(worksheet[cellAddress]?.v || '');
      }
      // Only push the row data if Release Project and Release Name are not empty.
      if (rowData[0].trim() !== '' && rowData[1].trim() !== '') {
        extractedData.push(rowData);
      }
    }

    return extractedData;
  }

  function handleFileUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files && target.files[0];
    const reader = new FileReader();

    reader.onload = (event: ProgressEvent<FileReader>) => {
      const fileData = extractFileData(event);

      $deploymentDetails = fileData.map(
        (item: any) => new DeploymentDetail(item[0], item[1], item[2] === '' ? null : item[2], item[3] === '' ? null : item[3], decodeBooleanValue(item[4])),
      );

      dispatch('onDeploymentDetailsUpload');
    };

    reader.readAsArrayBuffer(file);
    target.value = '';
  }
</script>

<div class="mb-1 mt-1 w-full">
  <input id="file-upload" type="file" accept=".xlsx, .xls" on:change={handleFileUpload} class="inputfile" />

  <label
    for="file-upload"
    class="bg-transparent hover:bg-blue-700 text-blue-900 dark:text-blue-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
  >
    Upload Excel File
  </label>
</div>

<style lang="scss">
  .inputfile {
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
  }

  .inputfile:focus + label {
    outline: 10px;
    box-shadow: var(--tw-ring-inset) 0 0 0 calc(1px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    border-color: #3b82f6;
  }
</style>
