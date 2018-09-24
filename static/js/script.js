
    $(document).ready(function () {
        $("#form1").submit(function () {
            $(".generar").attr("disabled", true);
            return true;
        });
    });

    $("#first-choice").change(function () {

        var $dropdown = $(this);

        $.getJSON("JSON/data.json", function (data) {

            var key = $dropdown.val();
            var vals = [];

            switch (key) {
                case 'Educacion':
                    vals = data.Educacion.split(",");
                    break;
                case 'Salud':
                    vals = data.Salud.split(",");
                    break;
                case 'base':
                    vals = ['Primero seleccione Categoria'];
            }

            var $secondChoice = $("#second-choice");
            $secondChoice.empty();
            $.each(vals, function (index, value) {
                $secondChoice.append("<option>" + value + "</option>");
            });

        });
    });
