const processorRadioGroup = document.querySelectorAll('input[name="processor_choice"]');
const mcs51Options = document.querySelector('#mcs51-options');
const stm8Options = document.querySelector('#stm8-options');
const z80Options = document.querySelector('#z80-options');
const dependentFieldsetLegend = document.querySelector('#dependent > legend');

processorRadioGroup.forEach((radio) => {
    radio.addEventListener('change', (event) => {
        const selectedProcessor = event.target.value;
        if (selectedProcessor === '-mmcs51') {
            dependentFieldsetLegend.textContent = 'MCS51 Options:';
            mcs51Options.style.display = 'block';
            stm8Options.style.display = 'none';
            z80Options.style.display = 'none';
        } else if (selectedProcessor === '-mz80') {
            dependentFieldsetLegend.textContent = 'Z80 Options:';
            mcs51Options.style.display = 'none';
            stm8Options.style.display = 'none';
            z80Options.style.display = 'block';
        } else if (selectedProcessor === '-mstm8') {
            dependentFieldsetLegend.textContent = 'STM8 Options:';
            mcs51Options.style.display = 'none';
            stm8Options.style.display = 'block';
            z80Options.style.display = 'none';
        }
    })
})