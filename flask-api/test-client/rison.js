// export default function RisonEncoder() {
module.exports = function RisonEncoder() {

  var sq = {"'" : true, '!' : true};
  var not_idstart = '-0123456789';
  var not_idchar = " '!:(),*@$";
  var idrx = '[^' + not_idstart + not_idchar + '][^' + not_idchar + ']*';
  var id_ok = new RegExp('^' + idrx + '$');
  var next_id = new RegExp(idrx, 'g');

  var enc = function(v) {
    if (v && typeof v.toJSON === 'function')
      v = v.toJSON();
    var fn = s[typeof v];
    if (fn)
      return fn(v);
  };

  const quote = function(x) {
    if (/^[-A-Za-z0-9~!*()_.',:@$\/]*$/.test(x))
        return x;

    return encodeURIComponent(x)
        .replace(/%2C/g, ',')
        .replace(/%3A/g, ':')
        .replace(/%40/g, '@')
        .replace(/%24/g, '$')
        .replace(/%2F/g, '/')
        .replace(/%20/g, '+');
  };

  var s = {
    array : function(x) {
      var a = [ '!(' ], b, f, i, l = x.length, v;
      for (i = 0; i < l; i += 1) {
        v = enc(x[i]);
        if (typeof v == 'string') {
          if (b) {
            a[a.length] = ',';
          }
          a[a.length] = v;
          b = true;
        }
      }
      a[a.length] = ')';
      return a.join('');
    },
    'boolean' : function(x) {
      if (x)
        return '!t';
      return '!f';
    },
    'null' : function() { return '!n'; },
    number : function(x) {
      if (!isFinite(x))
        return '!n';
      // strip '+' out of exponent, '-' is ok though
      return String(x).replace(/\+/, '');
    },
    object : function(x) {
      if (x) {
        if (x instanceof Array) {
          return s.array(x);
        }
        // WILL: will this work on non-Firefox browsers?
        if (typeof x.__prototype__ === 'object' &&
            typeof x.__prototype__.encode_rison !== 'undefined')
          return x.encode_rison();

        var a = [ '(' ], b, i, v, k, ki, ks = [];
        for (i in x)
          ks[ks.length] = i;
        ks.sort();
        for (ki = 0; ki < ks.length; ki++) {
          i = ks[ki];
          v = enc(x[i]);
          if (typeof v == 'string') {
            if (b) {
              a[a.length] = ',';
            }
            k = isNaN(parseInt(i)) ? s.string(i) : s.number(i)
            a.push(k, ':', v);
            b = true;
          }
        }
        a[a.length] = ')';
        return a.join('');
      }
      return '!n';
    },
    string : function(x) {
      if (x === '')
        return "''";

      if (id_ok.test(x))
        return x;

      x = x.replace(/(['!])/g, function(a, b) {
        if (sq[b])
          return '!' + b;
        return b;
      });
      return "'" + x + "'";
    },
    undefined : function() {
      // ignore undefined just like JSON
      return;
    }
  };

  this.encode = function(v) { return enc(v); };

  this.encode_array = function(v) {
    if (!(Array.isArray(v)))
      throw new error('rison.encode_array expects an array argument');
    var r = s[typeof v](v);
    return r.substring(2, r.length - 1);
  };

  this.encode_object = function(v) {
    if (typeof v != 'object' || v === null || v instanceof Array)
      throw new Error('rison.encode_object expects an object argument');
    var r = s[typeof v](v);
    return r.substring(1, r.length - 1);
  };

  this.encode_uri = function(v) { return quote(s[typeof v](v)); };
}

require('./rison.js')() 

// var rison = new RisonEncoder();
// console.log(rison.encode({any : "json", yes : true}));
// console.log(rison.encode_array([ "A", "B", {supportsObjects : true} ]));
// console.log(rison.encode_object({supportsObjects: true, ints: 435}));
// console.log(rison.encode_uri("http://www.abc.com"));
