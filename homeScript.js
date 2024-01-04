$(document).ready( 
    function(){
        var inputsVisible = false;

        $.ajax({
            url: '/molecules.db/Molecules',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $.each(data, function(index, element) {
                    var row = $('<tr>')
                    var col = $('<td>').text(element.NAME)
                    row.append(col)
                    var col = $('<td>').text(element.ATOM_NO)
                    row.append(col)
                    var col = $('<td>').text(element.BOND_NO)
                    row.append(col)
                    $('#table tbody').append(row)
                })
            }
        })

        $("#element_button").click(
            function(){
                location.href = './elements'
            }
        )

        $('form').submit(function(event) {
            event.preventDefault(); // prevent the form from submitting normally
            
            var moleculeName = $('#moleculeName').val(); // get the molecule name
            var sdfFile = $('#sdfFile').prop('files')[0]; // get the sdf file
            
            if (moleculeName == ""){
                alert('Please enter a molecule name');
                return;
            }

            // check if the file is an sdf file
            var ext = sdfFile.name.split('.').pop().toLowerCase();
            if (ext !== 'sdf') {
                alert('Please select an SDF file');
                return;
            }
            
            console.log("end of old stuff")

            var formData = new FormData()
            formData.append("moleculeName", moleculeName)
            formData.append("sdfFile", sdfFile)

            $.ajax({
              url: '/molecule',
              type: 'POST',
              data: formData,
              processData: false,
              contentType: false,
              success: function(data){
                alert('Molecule submitted successfully');
                var row = $('<tr>')
                var col = $('<td>').text(data.name)
                row.append(col)
                var col = $('<td>').text(data.atoms)
                row.append(col)
                var col = $('<td>').text(data.bonds)
                row.append(col)
                $('#table tbody').append(row)
              }
            })
            
        });

        $(document).on('dblclick', 'tbody tr', function() {
            // Get the first cell value of the clicked row
            var name = $(this).find('td:first').text();
          
            // Exclude the header row from being clickable
            if (name !== 'Name') {
              // Send the title to the server using AJAX
              $.post('/display', { 'name': name }, function(data) {
                // Parse the SVG data returned by the server
                console.log(data)
                var svgData = $(data).find('svg')[0].outerHTML;

                // Update the HTML to display the SVG image
                $('#svg_box').html(svgData);
              });
            }
            if (inputsVisible == false){
                inputsVisible = true
                $('#rotation_inputs').show();
            }

        });

        $("#rotate_button").click(function(){
       
            if ($('#xrotation').val().length === 0) {
                $('#xrotation').val('0');
              }
              
              if ($('#yrotation').val().length === 0) {
                $('#yrotation').val('0');
              }
              
              if ($('#zrotation').val().length === 0) {
                $('#zrotation').val('0');
              }

            if(!$.isNumeric($('#xrotation').val()) ||
                !$.isNumeric($('#yrotation').val()) ||
                !$.isNumeric($('#zrotation').val())) {
                alert("The input you entered is not valid.")
                return
            }
            $.post('/rotate', { xrot: $("#xrotation").val(),
                                 yrot: $("#yrotation").val(),
                                 zrot: $("#zrotation").val() },
                function(data) {
                    // Parse the SVG data returned by the server
                    console.log(data)
                    var svgData = $(data).find('svg')[0].outerHTML;

                    // Update the HTML to display the SVG image
                    $('#svg_box').html(svgData);
              });
    })
    }
);