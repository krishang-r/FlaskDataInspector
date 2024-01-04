document.addEventListener('DOMContentLoaded', function () {
  const fieldName = document.getElementById('field_name');
  const dataType = document.getElementById('data_type');
  const data = document.getElementById('data');
  const op = document.getElementById('op');
  const Enum = document.getElementById('Enum');
  const num = document.getElementById('num');
  const thresh = document.getElementById('thresh');

  const floatBlock = document.getElementById('Float');
  floatBlock.style.display = 'none';
  const stringBlock = document.getElementById('String');
  stringBlock.style.display = 'none';
  const operationYesBlock = document.getElementById('operation_yes');
  operationYesBlock.style.display = 'none';
  const operationNoBlock = document.getElementById('operation_no');
  operationNoBlock.style.display = 'none';
  // const submitButton = document.getElementById('submit');
  // submitButton.style.display = 'block';

  // Function to handle changes in op value
  function handleOpChange() {
      if (op.value === "1") {
          operationYesBlock.style.display = 'block';
          operationNoBlock.style.display = 'none';
      } else if (op.value === "0") {
          operationYesBlock.style.display = 'none';
          operationNoBlock.style.display = 'block';
      } else {
          operationYesBlock.style.display = 'none';
          operationNoBlock.style.display = 'none';
      }
  }

  function handleDataTypeChange() {
      if (dataType.value === "0") {
          data.value = "None";
          stringBlock.style.display = 'none';
          floatBlock.style.display = 'block';
      } else if (dataType.value === "1") {
          operationYesBlock.style.display = 'none';
          operationNoBlock.style.display = 'none';
          stringBlock.style.display = 'block';
          floatBlock.style.display = 'none';
      } else {
          stringBlock.style.display = 'none';
          floatBlock.style.display = 'none';
      }
  }

  // Event listener for dataType change
  dataType.addEventListener('change', handleDataTypeChange);

  // Event listener for op change
  op.addEventListener('change', handleOpChange);

  // Initial call to handleOpChange in case op has a default value
  handleDataTypeChange();
  handleOpChange();
});
