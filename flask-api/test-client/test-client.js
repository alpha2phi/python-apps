// Insert faker accounts
const faker = require("faker");
const axios = require('axios');

for (i = 0; i < 15; i++) {
    axios.post('http://localhost:5000/api/v1/accounts', {
        username: faker.name.findName(),
        email: faker.internet.email(),
        password: faker.internet.password()
    })
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });
}

// Search for alpha2phi
var filter = {};
filter.col = "email";
filter.opr = "eq";
filter.value = "alpha2phi@gmail.com";

var filters = [];
filters.push(filter);

filters_criteria = JSON.stringify({"filters" : filters});
console.log(encodeURI(filters_criteria));

const query = "http://localhost:5000/api/v1/accounts/?q=" + encodeURI(filters_criteria)
axios.get(query)
  .then(response => {
    console.log(response.data);
    // console.log(response.data.explanation);
  })
  .catch(error => {
    console.log(error);
  });
