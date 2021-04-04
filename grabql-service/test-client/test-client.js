const {request, gql} = require('graphql-request');
const fs = require("fs");

const query = gql`
  {
    screenshot(url: "http://www.medium.com", width:1024, height:768)
  }
`

const endpoint = 'http://localhost:8088';

request(endpoint, query).then((data) => {
  console.log(data.screenshot);
  const buffer = Buffer.from(data.screenshot, "base64");
  fs.writeFileSync("screenshot.png", buffer);
});
