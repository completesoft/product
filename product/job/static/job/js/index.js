      function addBlock(source, destination, forms_counter, init_forms){

          var currentcount = parseInt($(forms_counter).val());
          var block = $(source).clone();

          block.find("*").each(function(){
              var current_id = $(this).attr("id");
              var current_for = $(this).attr("for");
              var current_name = $(this).attr("name");

              if (current_id) {
                $(this).attr("id",  current_id.replace("0", currentcount));
                $(this).val("");
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

          if ($(block).attr('id')=="education_block"){
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
          if ($(block).attr('id')=="exp_block"){
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
        link_edu_start = "id_education-0-start_date";
        link_edu_end = "id_education-0-end_date";
        $("#edu_start_0").datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_edu_start,
          linkFormat: "dd.mm.yyyy"
         });
        $("#edu_end_0").datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_edu_end,
          linkFormat: "dd.mm.yyyy"
         });
        link_exp_start = "id_expirience-0-exp_start_date";
        link_exp_end = "id_expirience-0-exp_end_date";
        $("#exp_start_0").datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_exp_start,
          linkFormat: "dd.mm.yyyy"
         });
        $("#exp_end_0").datetimepicker({
          format: "MM yyyy",
          weekStart: 1,
          startView: 4,
          minView: 3,
          language: "ru",
          autoclose: true,
          linkField: link_exp_end,
          linkFormat: "dd.mm.yyyy"
         });
      }



      $(document).ready(function(){

          $("#addr").hide();


          $("#hide").click(function(){
              $("#addr").hide(500);
          });

          $("#show").click(function(){
              $("#addr").show(500);
              $("#addr").focus();
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
            addBlock("#education_block", "#education_div", "#id_education-TOTAL_FORMS", "#id_education-INITIAL_FORMS");
            $('input[name*=start_date], input[name*=end_date]').prop('readonly', true);
          });



          $("#add_exp").click(function() {
            addBlock("#exp_block", "#exp_div", "#id_expirience-TOTAL_FORMS", "#id_expirience-INITIAL_FORMS");
            $('input[name*=start_date], input[name*=end_date]').prop('readonly', true);
          });

      });