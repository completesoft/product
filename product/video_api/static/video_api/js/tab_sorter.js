(function($) {


$(document).ready(function(){
   var table = $('#table').DataTable({
        "responsive": true,
        "autoWidth": false,
        "stateSave": true,
        "stateDuration": 0,
        "fnInitComplete": function(oSettings, json) {
                var cols = oSettings.aoPreSearchCols;
                for (var i = 0; i < cols.length; i++) {
                    var value = cols[i].sSearch;
                    if (value.length > 0) {
                        $("tfoot th")[i].children[0].value = value;
                    }
                }
        },
        "language": {
            "lengthMenu": "Показать _MENU_ строк",
            "zeroRecords": "Нет данных удовлетворяющих условиям поиска",
            "search": "Поиск:",
            "info": "Показано с _START_ по _END_ из _TOTAL_ записей",
            "paginate": {
                "first":      "Первую",
                "last":       "Последняя",
                "next":       "Следующая",
                "previous":   "Предыдущая"
            },
        },
        "lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "ВСЕ"] ],
        'pageLength': 25,
        "columnDefs": [
            {
                'targets' : 0,
                render: function ( data, type, row, meta ) {
                    var dateSplit = data.split('.');
                    return type === "sort" ? dateSplit[2] +'-'+ dateSplit[1] +'-'+ dateSplit[0] : data;
                }
            }
        ]
   });


   table.columns().every( function () {
        var that = this;
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that.search( this.value ).draw();
            }
        });
   });


   $('#id_date_at').datetimepicker({
            format: "dd.mm.yyyy",
            weekStart: 1,
            startView: 3,
            minView: 2,
            language: "ru",
            autoclose: true,
            startDate: "-2y",
            endDate: "-0d",
            todayBtn: true,
            clearBtn: true,
          });
          $('#id_date_at').prop('readonly', true);

   $('#id_date_to').datetimepicker({
            format: "dd.mm.yyyy",
            weekStart: 1,
            startView: 3,
            minView: 2,
            language: "ru",
            autoclose: true,
            startDate: "-2y",
            endDate: "-0d",
            todayBtn: true,
            clearBtn: true,
          });
          $('#id_date_to').prop('readonly', true);



});
})(jQuery);