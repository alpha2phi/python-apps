var filter = {};
filter.col = "email";
filter.opr = "eq";
filter.value = "alpha2phi@gmail.com";

var filters = [];
filters.push(filter);

filters_criteria = JSON.stringify({"filters" : filters});
console.log(encodeURI(filters_criteria));

const query = "http://localhost:5000/api/v1/accounts/?q=" + encodeURI(filters_criteria)
const axios = require('axios');
axios.get(query)
  .then(response => {
    console.log(response.data);
    // console.log(response.data.explanation);
  })
  .catch(error => {
    console.log(error);
  });
