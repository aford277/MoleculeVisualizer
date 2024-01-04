$(document).ready(
    function(){

        $.ajax({
            url: '/molecules.db/Elements',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $.each(data, function(index, element) {
                    var row = $('<tr>')
                    var col = $('<td>').text(element.ELEMENT_NO)
                    row.append(col)
                    var col = $('<td>').text(element.ELEMENT_CODE)
                    row.append(col)
                    var col = $('<td>').text(element.ELEMENT_NAME)
                    row.append(col)
                    var col = $('<td>').text(element.COLOUR1)
                    row.append(col)
                    var col = $('<td>').text(element.COLOUR2)
                    row.append(col)
                    var col = $('<td>').text(element.COLOUR3)
                    row.append(col)
                    var col = $('<td>').text(element.RADIUS)
                    row.append(col)
                    $('#table tbody').append(row)
                })
            }
        })

        $("#add_button").click(
            function(){

                if($("#add_number").val() == "" ||
                $("#add_code").val() == "" ||
                $("#add_name").val() == "" ||
                $("#add_colour_1").val() == "" ||
                $("#add_colour_2").val() == "" ||
                $("#add_colour_3").val() == "" ||
                $("#add_radius").val() == ""){
                    alert("One or more input boxes are empty")
                    return
                }

                $.ajax({
                    url: "/add_element",
                    method: "POST",
                    data: {
                        num: $("#add_number").val(),
                        code: $("#add_code").val(),
                        name: $("#add_name").val(),
                        colour1: $("#add_colour_1").val(),
                        colour2: $("#add_colour_2").val(),
                        colour3: $("#add_colour_3").val(),
                        radius: $("#add_radius").val()
                    },
                    dataType: "text", // specify the expected data type
                    success: function(response) {
                        var table = document.getElementById("table");
                        var row = table.insertRow(-1);
                        var cell = row.insertCell(0);
                        cell.innerHTML = $("#add_number").val();
                        cell = row.insertCell(1);
                        cell.innerHTML = $("#add_code").val();
                        cell = row.insertCell(2);
                        cell.innerHTML = $("#add_name").val();
                        cell = row.insertCell(3);
                        cell.innerHTML = $("#add_colour_1").val();
                        cell = row.insertCell(4);
                        cell.innerHTML = $("#add_colour_2").val();
                        cell = row.insertCell(5);
                        cell.innerHTML = $("#add_colour_3").val();
                        cell = row.insertCell(6);
                        cell.innerHTML = $("#add_radius").val();
                    },
                    error: function(xhr, status, error) {
                        alert("Error: The element could not be added. This may be because the element already exists or your data may not be correct.")
                    }
                })
            }
        )

        $("#remove_button").click(
            function(){
                if($("#remove_code").val() == ""){
                    alert("Input box is empty")
                    return
                }

                $.ajax({
                    url: "/remove_element",
                    method: "POST",
                    data: {
                        code: $("#remove_code").val()
                    },
                    dataType: "text", // specify the expected data type
                    success: function(data, status){
                        $('#table tr').each(function(){
                            if($(this).find('td:eq(1)').text() == $("#remove_code").val()){
                                $(this).remove()
                            }
                        })
                    },
                    error: function(xhr, status, error) {
                        alert("Error: The element could not be removed.")
                    }
                })
            }
        )

        $("#back_button").click(
            function(){
                location.href = "./"
            }
        )
    }
);