var RisonEncoder = require("./rison.js");

var rison = new RisonEncoder()

console.log(rison.encode({any : "json", yes : true}));
console.log(rison.encode_array([ "A", "B", {supportsObjects : true} ]));
console.log(rison.encode_object({supportsObjects: true, ints: 435}));
console.log(rison.encode_uri("http://www.abc.com"));

