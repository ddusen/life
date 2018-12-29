// App = {
//   admin:{
//     dashboard:function(){
//       alert("haha");
//     },
//   },
//   common: {
//     init: function() {

//     },
// }

// UTIL = {
//   fire: function(func, funcname, args) {
//     var namespace = App // indicate your obj literal namespace here

//     funcname = (funcname === undefined) ? 'init' : funcname
//     if (func !== '' && namespace[func] && typeof namespace[func][funcname] == 'function') {
//       namespace[func][funcname](args)
//     }
//   },

//   loadEvents: function() {
//     var parent = window.location.pathname.split('/')[1]
//     var child = window.location.pathname.split('/')[2]
//     child = isNaN(Number(child)) ? child : 'id'

//     // hit up common first.
//     UTIL.fire('common')

//     // hit up parent first.
//     UTIL.fire(parent, child)

//     // do all the classes too.
//     // $.each(document.body.className.split(/\s+/), function(i, classnm) {
//     //   UTIL.fire(classnm)
//     //   UTIL.fire(classnm, parent)
//     // });

//     // UTIL.fire('common', 'finalize')
//   }
// };

// // kick it all off here
// $(document).ready(UTIL.loadEvents)