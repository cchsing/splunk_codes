require([
    './mylib1.js',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/searchmanager',
    'splunkjs/mvc/singleview',
    "splunkjs/mvc/simplexml/ready!"
], function(mylib1,$,mvc,SearchManager,SingleView) { 

    var search_1 = new SearchManager({
        id: "search_1",
        earliest_time: "-24h@h",
        latest_time: "now",
        preview: true,
        cache: false,
        search: "index=_internal sourcetype=splunkd_ui_access | timechart count" 
    });

    var myResults = search_1.data('results');
    search_1.on('search:done',function(properties){
        myResults = search_1.data('results');
    });
    
    var singleV_1 = new SingleView({
        id: "singleV_1",
        managerid: "search_1",
        el: $("#screen_2")
    }).render();

    $(document).ready(function() {
        var var_1 = 0;
        var var_2 = 0;
        $("#btn_1").on("click", function(){
            if (var_1 == 0) {
                var_1 = 1;
                $("#img1").attr("src","/static/app/test_app_splunk/1F600.svg");
                // console.log(search_1.data('results'));
                // console.log(myResults.data().rows[myResults.data().rows.length - 1]);
                // console.log(myResults.data().rows[myResults.data().rows.length - 1][1]);
                // console.log("The value holder: ", var_2);
            } else {
                var_1 = 0;
                $("#img1").attr("src","/static/app/test_app_splunk/1F621.svg");
            };
        });
        
        if (var_2 >= 200) {
            $("#img2").attr("src","/static/app/test_app_splunk/foodpanda.png");
        } else {
            $("#img2").attr("src","/static/app/test_app_splunk/1F621.svg");
        }

        setInterval(function() {
            search_1.startSearch();
            var_2 = myResults.data().rows[myResults.data().rows.length - 1][1];
        }, 10000);
    });

 });