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

    var singleV_1 = new SingleView({
        id: "singleV_1",
        managerid: "search_1",
        el: $("#screen_2")
    }).render();

    var var_1 = 0;
    $(document).ready(function() {
        $("#btn_1").on("click", function(){
            if (var_1 == 0) {
                var_1 = 1;
                $("#img1").attr("src","/static/app/test_app_splunk/1F600.svg");
            } else {
                var_1 = 0;
                $("#img1").attr("src","/static/app/test_app_splunk/1F621.svg");
            };
        });
    });

 });