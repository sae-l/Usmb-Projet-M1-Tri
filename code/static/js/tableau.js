$(document).ready(function () {
    $('#tab').DataTable({
        scrollY:        '55vh',
        scrollCollapse: true,
        paging:         false,
        "language": {
            "lengthMenu": "Affichage de _MENU_ résultats par page",
            "zeroRecords": "Aucun résultat ici! Désolé",
            "infoEmpty": "Aucun résultat disponible",
            "infoFiltered": "(filtré à partir de _MAX_ résultats)",
            "info": "Affichage de _TOTAL_ entrées",
            "search": "Recherche :"
        }
    } );
});

$(document).ready(function () {
    $('.dtable').DataTable({
        scrollY:        '55vh',
        scrollCollapse: true,
        paging:         false,
        "language": {
            "lengthMenu": "Affichage de _MENU_ résultats par page",
            "zeroRecords": "Aucun résultat ici! Désolé",
            "infoEmpty": "Aucun résultat disponible",
            "infoFiltered": "(filtré à partir de _MAX_ résultats)",
            "info": "Affichage de _TOTAL_ entrées",
            "search": "Recherche :"
        }
    } );
});