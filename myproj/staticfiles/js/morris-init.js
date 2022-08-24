$( function () {
    "use strict";
// Morris donut chart
Morris.Donut( {
    element: 'morris-donut-chart', data: [ {
        label: "Completed", value: 20,
    }
    , {
        label: "In-progress", value: 10
    }
    , {
        label: "Pending", value: 9
    }
    ], resize: true, colors: [ '#00bcd2', '#424858', '#ffcdd3']
}
);
// Extra chart
Morris.Area( {
    element: 'extra-area-chart', data: [ {
        user: '2019', completed: 10, pending: 3, inprogress: 5
    }
    , {
        user: '2020', completed: 6, pending: 2, inprogress: 2
    }
    , {
        user: '2021', completed: 4, pending: 2, inprogress: 3
    }
    , {
        user: '2022', completed: 4, pending: 2, inprogress: 3
    }
    
    ], lineColors: [ '#2e61f2', '#424858', '#ff5450'], xkey: 'user', ykeys: [ 'completed', 'pending', 'inprogress'], labels: [ 'completed', 'pending', 'in-progress'], pointSize: 0, lineWidth: 0, resize: true, fillOpacity: 0.8, behaveLikeLine: true, gridLineColor: '#e0e0e0', hideHover: 'auto'
}
);

}

);