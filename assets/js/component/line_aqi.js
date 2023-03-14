
    var line_aqi_chart01 = echarts.init(document.getElementById("line_aqi_chart_01"), theme_name);

    function line_aqi_chart01_show(input_adcode) {
        $.get('./data/line_aqi_data/line_aqi_' + input_adcode + '.json', function (data) {
            line_aqi_chart01.setOption(
                {
                    title: {
                        text: adcode_info[input_adcode].name + ' AQI',
                        left: '300px',
                        top: '20px'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    grid: {
                        left: '5%',
                        right: '15%',
                        bottom: '10%'
                    },
                    xAxis: {
                        data: data.map(function (item) {
                            return item[0];
                        })
                    },
                    yAxis: {},

                    dataZoom: [
                        {
                            startValue: '2013-01-01'
                        },
                        {
                            type: 'inside'
                        }
                    ],
                    visualMap: {
                        top: 50,
                        right: 150,
                        pieces: [
                            {
                                gt: 0,
                                lte: 50,
                                color: '#93CE07'
                            },
                            {
                                gt: 50,
                                lte: 100,
                                color: '#FBDB0F'
                            },
                            {
                                gt: 100,
                                lte: 150,
                                color: '#FC7D02'
                            },
                            {
                                gt: 150,
                                lte: 200,
                                color: '#FD0100'
                            },
                            {
                                gt: 200,
                                lte: 300,
                                color: '#AA069F'
                            },
                            {
                                gt: 300,
                                color: '#AC3B2A'
                            }
                        ],
                        outOfRange: {
                            color: '#999'
                        }
                    },
                    series: {
                        name: adcode_info[input_adcode].name + ' AQI',
                        type: 'line',
                        data: data.map(function (item) {
                            return {'value': item[1], 'time': item[0]};
                        }),
                        //mark
                        markLine: {
                            silent: true,
                            lineStyle: {
                                color: '#333'
                            },
                            data: [
                                {
                                    yAxis: 50
                                },
                                {
                                    yAxis: 100
                                },
                                {
                                    yAxis: 150
                                },
                                {
                                    yAxis: 200
                                },
                                {
                                    yAxis: 300
                                }
                            ]
                        }
                    }
                }
            );
        });
    }

    line_aqi_chart01_show(110102)