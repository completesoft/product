$(document).ready(function(){

    $('#id_date_at').datetimepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        startView: 4,
        minView: 2,
        language: "ru",
        autoclose: true,
        startDate: "-70y",
        endDate: new Date(),
      });
//      $('#id_date_at').prop('readonly', true);

    $('#id_date_to').datetimepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        startView: 4,
        minView: 2,
        language: "ru",
        autoclose: true,
        startDate: "-70y",
        endDate: new Date(),
      });
//      $('#id_date_to').prop('readonly', true);





});