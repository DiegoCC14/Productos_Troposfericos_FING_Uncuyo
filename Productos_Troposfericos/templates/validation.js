// show a message with a type of the input
function showMessage(input, message, type, reset = false) {
  // get the small element and set th message

  const msg = input.parentNode.parentNode.querySelector("small");
  msg.innerText = message;
  if (reset) {
    input.style.borderColor = "#ccd1d1";
  } else {
    if (message != "") {
      input.style.borderColor = "red";
      // update the class for the input
    } else {
      input.style.borderColor = "green";
    }
  }
  return type;
}

function showError(input, message) {
  return showMessage(input, message, false);
}

function showSuccess(input) {
  return showMessage(input, "", true);
}

function hasValue(input, message, merror = true) {
  if (input.value.trim() === "") {
    if (merror) {
      return showError(input, message);
    } else {
      return false;
    }
  }
  if (merror) {
    return showSuccess(input);
  } else {
    return true;
  }
}

function validateEstacion(input, requiredMsg, invalidMsg, merror = true) {
  // check if the value is not empty
  if (!hasValue(input, requiredMsg, merror)) {
    return false;
  }
  // validate email format
  const estacionRegex = /^((([A-Z]|[a-z]|[0-9]){4}(,)?)|(TRUET))*$/;

  const estacion = input.value.trim();
  if (!estacionRegex.test(estacion)) {
    return showError(input, invalidMsg);
  }
  return true;
}

function validateLongitud(input, requiredMsg, invalidMsg, merror = true) {
  // check if the value is not empty
  if (!hasValue(input, requiredMsg, merror)) {
    return false;
  }
  // validate email format
  const estacionRegex =
    /^(((((([0-9]){1,2}|(^[1][0-7][0-9]))|(180))|^[-]((([0-9]){1,2}|([1][0-7][0-9]))|(180)))[./][0-9]*)|((((([0-9]){1,2}|(^[1][0-7][0-9]))|(180))|^[-]((([0-9]){1,2}|([1][0-7][0-9]))|(180)))[./]?)|(TRUET))$/;

  const estacion = input.value.trim();
  if (!estacionRegex.test(estacion)) {
    if (merror) {
      return showError(input, invalidMsg);
    } else {
      return false;
    }
  }
  return true;
}

function validateLatitud(input, requiredMsg, invalidMsg, merror = true) {
  // check if the value is not empty
  if (!hasValue(input, requiredMsg, merror)) {
    return false;
  }
  // validate email format
  const estacionRegex =
    /^(((((^[0-8][0-9])|([0-9])|(^[0][0-9])|(^[9][0]))|^[-](([0-8][0-9])|([0-9])|([0][0-9])|([9][0])))[./][0-9]*)|((((^[0-8][0-9])|([0-9])|(^[0][0-9])|(^[9][0]))|^[-](([0-8][0-9])|([0-9])|([0][0-9])|([9][0])))[./]?)|(TRUET))$/;

  const estacion = input.value.trim();
  if (!estacionRegex.test(estacion)) {
    if (merror) {
      return showError(input, invalidMsg);
    } else {
      return false;
    }
  }
  return true;
}

var form = document.querySelector("#Search");
//var form = $("#Search");
$(document).ready(function () {
  
  var form = document.querySelector("#Search");

  $("#Estacionbutton").click(function () {
    $("#demo").collapse("toggle");
    $("#demo1").collapse("hide");
    form.elements["LN"].value = "";
    form.elements["LS"].value = "";
    form.elements["LE"].value = "";
    form.elements["LO"].value = "";
    form.elements["Estacion"].value = "";
    showMessage(form.elements["Estacion"], "", true, true);
    showMessage(form.elements["LN"], "", true, true);
    showMessage(form.elements["LS"], "", true, true);
    showMessage(form.elements["LO"], "", true, true);
    showMessage(form.elements["LE"], "", true, true);
  });

  $("#datetimepicker6").on("dp.change",function (e) {
	  $("#datetimepicker7")
      .data("DateTimePicker")
      .minDate(e.date);
  });
  $("#datetimepicker7").on("dp.change",function (e) {
	  $("#datetimepicker6")
      .data("DateTimePicker")
      .maxDate(e.date);
  });
  $("#Rangobutton").click(function () {
    $("#demo1").collapse("toggle");
    $("#demo").collapse("hide");
    form.elements["Estacion"].value = "";
    showMessage(form.elements["Estacion"], "", true, true);
    form.elements["LN"].value = "";
    form.elements["LS"].value = "";
    form.elements["LE"].value = "";
    form.elements["LO"].value = "";
    showMessage(form.elements["LN"], "", true, true);
    showMessage(form.elements["LS"], "", true, true);
    showMessage(form.elements["LO"], "", true, true);
    showMessage(form.elements["LE"], "", true, true);
  });
});

const FECHA_REQUIRED = "Por favor, coloque una fecha";
const ESTACION_REQUIRED = "Por favor, coloque una estación";
const ESTACION_INVALID =
  "Por favor, coloque la estación con el formato correcto: (AAAA) o (AAAA,BBBB,etc) para multiple estaciones";
const LONGITUD_REQUIRED = "Por favor, coloque una longitud";
const LONGITUD_INVALID =
  "Por favor coloque una longitud correcta (Recuerde que el rango es [-180,180])";
const LATITUD_REQUIRED = "Por favor, coloque una latitud";
const LATITUD_INVALID =
  "Por favor, coloque una latitud correcta (Recuerde que el rango es [-90,90])";
const CHECKBOX = "Por favor, indique al menos un producto a descargar";

function checkEstacion() {
  // stop form submission
  validateEstacion(
    form.elements["Estacion"],
    ESTACION_REQUIRED,
    ESTACION_INVALID
  );
}
function checkLN() {
  // stop form submission

  validateLatitud(form.elements["LN"], LATITUD_REQUIRED, LATITUD_INVALID);
  updateMaps();
}
function checkLS() {
  // stop form submission

  validateLatitud(form.elements["LS"], LATITUD_REQUIRED, LATITUD_INVALID);
  updateMaps();
}
function checkLO() {
  // stop form submission

  validateLongitud(form.elements["LO"], LONGITUD_REQUIRED, LONGITUD_INVALID);
  updateMaps();
}
function checkLE() {
  // stop form submission

  validateLongitud(form.elements["LE"], LONGITUD_REQUIRED, LONGITUD_INVALID);
  updateMaps();
}
function checkFecha() {
  hasValue( $("#Fecha1") , FECHA_REQUIRED );
  hasValue( $("#Fecha2") , FECHA_REQUIRED );
}
function updateMaps() {
  var LO = parseFloat(form.elements["LO"].value.trim());
  var LE = parseFloat(form.elements["LE"].value.trim());
  var LN = parseFloat(form.elements["LN"].value.trim());
  var LS = parseFloat(form.elements["LS"].value.trim());
  let LOValid2 = validateLongitud(
    form.elements["LO"],
    LONGITUD_REQUIRED,
    LONGITUD_INVALID,
    false
  );
  let LEValid2 = validateLongitud(
    form.elements["LE"],
    LONGITUD_REQUIRED,
    LONGITUD_INVALID,
    false
  );
  let LNValid2 = validateLatitud(
    form.elements["LN"],
    LATITUD_REQUIRED,
    LATITUD_INVALID,
    false
  );
  let LSValid2 = validateLatitud(
    form.elements["LS"],
    LATITUD_REQUIRED,
    LATITUD_INVALID,
    false
  );

  if (LOValid2 && LEValid2 && LNValid2 && LSValid2) {
    var Dlat = LN - LS;
    var Dlong = LO - LE;
    var c = Math.sqrt(Math.pow(Dlat, 2) + Math.pow(Dlong, 2));
    const view = map.getView();
    view.setResolution(c);
    view.setCenter(ol.proj.fromLonLat([(LO + LE) / 2, (LN + LS) / 2]));
  }
}
function pageReset() {
  form.elements["LN"].value = "";
  form.elements["LS"].value = "";
  form.elements["LE"].value = "";
  form.elements["LO"].value = "";
  showMessage(form.elements["LN"], "", true, true);
  showMessage(form.elements["LS"], "", true, true);
  showMessage(form.elements["LO"], "", true, true);
  showMessage(form.elements["LE"], "", true, true);
  showMessage(form.elements["Fecha1"], "", true, true);
  showMessage(form.elements["Fecha2"], "", true, true);
  form.elements["Estacion"].value = "";
  showMessage(form.elements["Estacion"], "", true, true);
  today = new Date();
  days = 86400000;
  var fecha = new Date(today - 30 * days);
  var dia = fecha.getDate();
  var mes = fecha.getMonth() + 1;
  var ano = fecha.getFullYear();
  var h = fecha.getHours();
  mes = "" + mes;
  if (mes.length == 1) {
    mes = "0" + mes;
  }
  var dateTime = ano + "-" + mes + "-" + dia + " " + h;
  $("#datetimepicker6").datetimepicker({
    viewMode: "years",
    format: "YYYY-MM-DD HH",
  });
  $("#datetimepicker7").datetimepicker({
    viewMode: "years",
    format: "YYYY-MM-DD  HH",
  });

  console.log(dateTime);
  $("#datetimepicker7").data("DateTimePicker").Date = dateTime;
  $("#datetimepicker6").data("DateTimePicker").Date = dateTime;
 
  $("#datetimepicker6").data("DateTimePicker").minDate("2013-01-01 00");
  $("#datetimepicker7").data("DateTimePicker").minDate("2013-01-01 00");
  $("#datetimepicker7").data("DateTimePicker").maxDate(dateTime);
  $("#datetimepicker6")
      .data("DateTimePicker")
      .maxDate(dateTime);
}
form.addEventListener("submit", function (event) {
  // stop form submission
  event.preventDefault();
  var estaciones = "";
  var LO = parseFloat(form.elements["LO"].value.trim());
  var LE = parseFloat(form.elements["LE"].value.trim());
  var LN = parseFloat(form.elements["LN"].value.trim());
  var LS = parseFloat(form.elements["LS"].value.trim());
  var Presion = document.querySelector("#Presion");
  var Temperatura = document.querySelector("#Temperatura");
  var IWV = document.querySelector("#IWV");
  var ZTD = document.querySelector("#ZTD");
  // validate the form
  let Fecha1Valid = hasValue(form.elements["Fecha1"], FECHA_REQUIRED);
  let Fecha2Valid = hasValue(form.elements["Fecha2"], FECHA_REQUIRED);
  let EstacionValid = validateEstacion(
    form.elements["Estacion"],
    ESTACION_REQUIRED,
    ESTACION_INVALID
  );
  let LOValid = validateLongitud(
    form.elements["LO"],
    LONGITUD_REQUIRED,
    LONGITUD_INVALID
  );
  let LEValid = validateLongitud(
    form.elements["LE"],
    LONGITUD_REQUIRED,
    LONGITUD_INVALID
  );
  let LNValid = validateLatitud(
    form.elements["LN"],
    LATITUD_REQUIRED,
    LATITUD_INVALID
  );
  let LSValid = validateLatitud(
    form.elements["LS"],
    LATITUD_REQUIRED,
    LATITUD_INVALID
  );
  // if valid, submit the form.
  if (Presion.checked || Temperatura.checked || IWV.checked || ZTD.checked) {
    showMessage(document.querySelector("#hh"), "", true, true);
    if (Fecha1Valid && Fecha2Valid && EstacionValid) {
      form.submit();
    }
    if (
      Fecha1Valid &&
      Fecha2Valid &&
      LOValid &&
      LEValid &&
      LNValid &&
      LSValid
    ) {
      for (var i = 0; i < stations.length; i++) {
        aux1 = parseFloat(stations[i]["longitude"]);
        aux2 = parseFloat(stations[i]["latitude"]);

        if (LO < aux1 && LE > aux1 && LS < aux2 && LN > aux2) {
          if (estaciones != "") {
            estaciones = estaciones + "," + stations[i]["name"];
          } else {
            estaciones = stations[i]["name"];
          }
        }
      }

      form.elements["Estacion"].value = estaciones;
      form.submit();
    }
  } else {
    showError(document.querySelector("#hh"), CHECKBOX);
  }
});

document.addEventListener("load", pageReset());
