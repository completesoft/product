
function addBlock(source, destination, forms_counter, init_forms){

  var currentcount = parseInt($(forms_counter).val());
  var block = $(source).clone();

  $(source).find("*").each(function(){
    var is_id = $(this).attr("id");
    if (is_id) {
        $(this).val("");
      }
  });

  block.find("*").each(function(){
      var current_id = $(this).attr("id");
      var current_for = $(this).attr("for");
      var current_name = $(this).attr("name");

      if (current_id) {
        $(this).attr("id",  current_id.replace("0", currentcount));
      }

      if (current_for) {
        $(this).attr("for", current_for.replace("0", currentcount));
      }

      if (current_name) {
        $(this).attr("name", current_name.replace("0", currentcount));
      }

  });

  $(forms_counter).val(currentcount+1);
  $(init_forms).val(currentcount+1);
  $(destination).append(block);

  link_start = $(block).find('input[id*=start_date]').attr('id');
  link_end = $(block).find('input[id*=end_date]').attr('id');
  console.log(link_start);


  if ($(block).attr('id')=="edu_add_source"){
    console.log('datetimepicker');
    $(block).find('input[id*=edu_start]').datetimepicker({
      format: "MM yyyy",
      weekStart: 1,
      startView: 4,
      minView: 3,
      language: "ru",
      autoclose: true,
      linkField: link_start,
      linkFormat: "dd.mm.yyyy"
     });
    $(block).find('input[id*=edu_end]').datetimepicker({
      format: "MM yyyy",
      weekStart: 1,
      startView: 4,
      minView: 3,
      language: "ru",
      autoclose: true,
      linkField: link_end,
      linkFormat: "dd.mm.yyyy"
     });
  }
  if ($(block).attr('id')=="exp_add_source"){
    $(block).find('input[id*=exp_start]').datetimepicker({
      format: "MM yyyy",
      weekStart: 1,
      startView: 4,
      minView: 3,
      language: "ru",
      autoclose: true,
      linkField: link_start,
      linkFormat: "dd.mm.yyyy"
     });
    $(block).find('input[id*=exp_end]').datetimepicker({
      format: "MM yyyy",
      weekStart: 1,
      startView: 4,
      minView: 3,
      language: "ru",
      autoclose: true,
      linkField: link_end,
      linkFormat: "dd.mm.yyyy"
     });
  }
}

    function addDateTimePicker(){

        var link_edu_start = "id_eduadd-0-start_date";
        var link_edu_end = "id_eduadd-0-end_date";
        $('#edu_add_source input[id*=edu_start_]').datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_edu_start,
          linkFormat: "dd.mm.yyyy"
         });
        $('#edu_add_source input[id*=edu_end_]').datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_edu_end,
          linkFormat: "dd.mm.yyyy"
         });
        var link_exp_start = "id_expadd-0-exp_start_date";
        var link_exp_end = "id_expadd-0-exp_end_date";
        $('#exp_add_source input[id*=exp_start_]').datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_exp_start,
          linkFormat: "dd.mm.yyyy"
         });
        $("input[id*=exp_end_]").datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_exp_end,
          linkFormat: "dd.mm.yyyy"
         });


        $('fieldset[count]').each(function(){
            var count = $(this).attr("count");
            console.log('IN DATE TIMEPICKER');

            if($(this).attr('formtype')=="edu"){
                var dest_start = 'edu_start_'+count;
                var dest_end = 'edu_end_'+count;
                var link_start = 'id_education-'+count+'-start_date';
                var link_end = 'id_education-'+count+'-end_date';
                $('#'+dest_start).datetimepicker({
                    format: "MM yyyy",
                    weekStart: 1,
                    startView: 4,
                    minView: 3,
                    language: "ru",
                    autoclose: true,
                    linkField: link_start,
                    linkFormat: "dd.mm.yyyy"
                });
                $('#'+dest_end).datetimepicker({
                    format: "MM yyyy",
                    weekStart: 1,
                    startView: 4,
                    minView: 3,
                    language: "ru",
                    autoclose: true,
                    linkField: link_end,
                    linkFormat: "dd.mm.yyyy"
                });
            }
            if($(this).attr('formtype')=="exp"){
                console.log('FORMTYPE EXP');
                var dest_start = 'exp_start_'+count;
                var dest_end = 'exp_end_'+count;
                var link_start = 'id_experience-'+count+'-exp_start_date';
                var link_end = 'id_experience-'+count+'-exp_end_date';
                console.log(link_start+'***'+link_end);
                $('#'+dest_start).datetimepicker({
                    format: "MM yyyy",
                    weekStart: 1,
                    startView: 4,
                    minView: 3,
                    language: "ru",
                    autoclose: true,
                    linkField: link_start,
                    linkFormat: "dd.mm.yyyy"
                });
                $('#'+dest_end).datetimepicker({
                    format: "MM yyyy",
                    weekStart: 1,
                    startView: 4,
                    minView: 3,
                    language: "ru",
                    autoclose: true,
                    linkField: link_end,
                    linkFormat: "dd.mm.yyyy"
                });
            }
        });
    }


  $(document).ready(function(){

      if (!$("#addr").val()){
        $("#addr").hide();
      };

      $("#hide").click(function(){
          $("#addr").hide(500);
      });

      $("#show").click(function(){
          $("#addr").show(500);
          $("#addr").focus();
      });

      $('#save_all').click(function() {
        $("#mainForm").submit();
      });

      $('#id_passp_date').datetimepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        startView: 4,
        minView: 2,
        language: "ru",
        autoclose: true,
        startDate: "-70y",
        endDate: new Date(),
      });
      $('#id_passp_date').prop('readonly', true);

      $('#id_start').datetimepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        startView: 2,
        minView: 2,
        language: "ru",
        autoclose: true,
        startDate: new Date()
      });
      $('#id_start').prop('readonly', true);

      $('#id_birthday').datetimepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        startView: 4,
        minView: 2,
        language: "ru",
        autoclose: true,
        startDate: "-80y",
        endDate: "-14y",
      });
      $('#id_birthday').prop('readonly', true);


      addDateTimePicker();
      $('input[name*=start_date], input[name*=end_date]').prop('readonly', true);


      $("#add_education").click(function() {
        addBlock("#edu_add_source", "#education_div", "#id_eduadd-TOTAL_FORMS", "#id_eduadd-INITIAL_FORMS");
        $('input[name*=start_date], input[name*=end_date]').prop('readonly', true);
      });


      $("#add_experience").click(function() {
        addBlock("#exp_add_source", "#experience_div", "#id_expadd-TOTAL_FORMS", "#id_expadd-INITIAL_FORMS");
        $('input[name*=start_date], input[name*=end_date]').prop('readonly', true);
      });
  });