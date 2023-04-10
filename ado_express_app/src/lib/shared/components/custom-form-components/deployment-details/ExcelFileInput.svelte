<script lang="ts">
  import * as XLSX from 'xlsx';
  import { DeploymentDetails } from '../../../../models/classes/deployment-details.model';

  export let deploymentDetails: DeploymentDetails[] = [];

  function getBooleanValue(isCrucialUserInput: String) {
    const trueValues = ['t', 'true', 'y', 'yes', '1'];

    return trueValues.includes(isCrucialUserInput.toLowerCase());
  }

  function handleFileUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files && target.files[0];
    const reader = new FileReader();

    reader.onload = (event: ProgressEvent<FileReader>) => {
      const data = new Uint8Array(event.target.result as ArrayBuffer);
      const workbook = XLSX.read(data, { type: 'array' });

      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      const range = XLSX.utils.decode_range(worksheet['!ref']);

      const excelData: string[][] = [];

      for (let rowNum = 1; rowNum <= range.e.r; rowNum++) {
        const rowData: string[] = [];

        for (let colNum = 0; colNum < 5; colNum++) {
          const cellAddress = XLSX.utils.encode_cell({ r: rowNum, c: colNum });
          rowData.push(worksheet[cellAddress]?.v || '');
        }

        excelData.push(rowData);
      }

      deploymentDetails = excelData.map(
        (item: any) =>
          new DeploymentDetails(
            item[0],
            item[1],
            item[2],
            item[3],
            getBooleanValue(item[4])
          )
      );
    };

    reader.readAsArrayBuffer(file);
    target.value = '';
  }
</script>

<div class="w-full mt-1 mb-1">
  <input
    type="file"
    id="file-upload"
    on:change={handleFileUpload}
    class="hidden"
    accept=".xlsx, .xls"
  />
  <label
    for="file-upload"
    class="bg-transparent hover:bg-blue-700 text-blue-900 font-semibold hover:text-white py-2 px-4 border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
  >
    Upload Excel File
  </label>
</div>
