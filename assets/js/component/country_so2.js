
    var so2_map_echart = echarts.init(document.getElementById("so2_map_echart"), theme_name);

    function so2_map_echart_show(year, month, day) {
        let year_month_day = year + ('0' + month).slice(-2) + ('0' + day).slice(-2)

        let wind_json_path = './data/so2_data/' + year + ('0' + month).slice(-2) + '/so2_' + year_month_day + '.json'

        $.getJSON(wind_json_path, function (data) {
            var shuffle = function (array) {
                var currentIndex = array.length;
                var temporaryValue;
                var randomIndex;
                // While there remain elements to shuffle...
                while (0 !== currentIndex) {
                    // Pick a remaining element...
                    randomIndex = Math.floor(Math.random() * currentIndex);
                    currentIndex -= 1;
                    // And swap it with the current element.
                    temporaryValue = array[currentIndex];
                    array[currentIndex] = array[randomIndex];
                    array[randomIndex] = temporaryValue;
                }
                return array;
            }
            // console.log(data)
            var maxMag = 0;
            var minMag = Infinity;

            data.forEach((val, index) => {
                if (minMag > val[2]) {
                    minMag = val[2]
                }
                if (maxMag < val[2]) {
                    maxMag = val[2]
                }
            })
            shuffle(data)
            // data = data.slice(0, Math.round(data.length / 2))
            // 数据优化算法，基于平均定理
            so2_map_echart.setOption(
                {
                    title: {
                        text: "全国SO2分布图 " + year + '-' + ('0' + month).slice(-2) + '-' + ('0' + day).slice(-2),
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: 'black'
                        }
                    },
                    backgroundColor: "rgba(254,248,239,1)",
                    visualMap: {
                        left: 'center',
                        min: 0,
                        max: 600,
                        dimension: 2,
                        inRange: {
                            // prettier-ignore
                            color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                        },
                        calculable: true,
                        textStyle: {
                            color: 'black'
                        },
                        orient: 'horizontal'
                    },
                    geo: {
                        map: '100000',
                        left: 0,
                        right: 0,
                        top: 0,
                        silent: true,
                        roam: true,
                        itemStyle: {
                            areaColor: '#323c48',
                            borderColor: '#111'
                        }
                    },
                    series: {
                        type: 'custom',
                        coordinateSystem: 'geo',
                        data: data,
                        encode: {
                            x: 0,
                            y: 0
                        },
                        renderItem: function (params, api) {
                            const x = api.value(0);
                            const y = api.value(1);
                            const start = api.coord([
                                x,
                                y
                            ]);
                            const bili = 0.1
                            const end = api.size([
                                bili,
                                bili
                            ]);
                            return {
                                type: 'rect',
                                shape: {
                                    x: start[0],
                                    y: start[1],
                                    width: end[0],
                                    height: end[1]
                                },
                                style: {
                                    fill: api.visual('color'),
                                    lineWidth: 0
                                }
                            };
                        },
                        progressive: 2000
                    }
                }
            );
        });
    }