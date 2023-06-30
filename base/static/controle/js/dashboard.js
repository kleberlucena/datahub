const dadosMissoesAoLogoDosMesesAnos = "http://127.0.0.1:8000/controle/obtem_dados_de_missoes_por_mes"
const dadosMissoesPorUsuario = "http://127.0.0.1:8000/controle/obtem_dados_de_missoes_por_usuario"
const ctx1 = document.getElementById('myChart1').getContext("2d");
const ctx2 = document.getElementById('myChart2').getContext("2d");

const yearSelect = document.getElementById("year-select");
let myChart = null;

onload = () => {
  getMissionsPerMonthData()
  .then(data => {
    displayMissions(data)
  })
  .catch((error) => {
    console.log("error na promise:", error);
  });

  getMissionsPerUserData().then(data => {
    displayResultadosEfetivo(data);
  })
  .catch((error) => {
    console.log(error);
  });
}

function updateYearData() {
  if(myChart != null) {
    myChart.destroy();
  }
  getMissionsPerMonthData()
  .then(data => {
    displayMissions(data)
  });
}

async function getMissionsPerMonthData() {
    const response = await fetch(dadosMissoesAoLogoDosMesesAnos);
    const data = await response.json();

    const years = Object.keys(data);
    const monthArrays = [];

    for (const year of years) {
      const months = [];
      const values = [];
      for (const month in data[year]) {
        months.push(month);
        values.push(data[year][month]);
      }
      monthArrays.push({ year, months, values });
    }

    let monthsValuesToBeLoaded = [];
    
    for(let i=0; i < monthArrays.length; i++) {
      if(monthArrays[i].year == yearSelect.value) {
        monthsValuesToBeLoaded.push(monthArrays[i].months);
        monthsValuesToBeLoaded.push(monthArrays[i].values);
      }
    }
    
    return monthsValuesToBeLoaded;
}

async function getMissionsPerUserData() {
  const response = await fetch(dadosMissoesPorUsuario);
  const data = await response.json();
  const missionsPerUsers = [];

  for (const [user, number] of Object.entries(data)) {
    missionsPerUsers.push({ user, number });
  }
  dadosNumeroDeMissoesPorUsuarios = []
  let usuarios = missionsPerUsers.map(missionsPerUsers => missionsPerUsers.user)
  let num_missoes = missionsPerUsers.map(missionsPerUsers => missionsPerUsers.number)
  dadosNumeroDeMissoesPorUsuarios.push(usuarios);
  dadosNumeroDeMissoesPorUsuarios.push(num_missoes);
  return dadosNumeroDeMissoesPorUsuarios;
}


function displayMissions(array) {
  myChart = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: array[0],
      datasets: [{
        label: `Missões em ${yearSelect.value}`,
        data: array[1],
        borderWidth: 3,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
      ],
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function displayResultadosEfetivo(array) {
  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: array[0],
      datasets: [{
        label: 'Nº de missões por piloto',
        data: array[1],
        borderWidth: 2,

      }]
    },
    options: {
      indexAxis: 'y',
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}