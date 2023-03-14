
    let radar_charts01 = echarts.init(document.getElementById("radar_charts01"), theme_name);

    function radar_charts01_show(adcode = '310000', year = 2013, month = 1, day = 1) {
        const project_name = ["AQI", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
        const project_limit_max = [350, 250, 420, 1000, 565, 36, 800]

        month = ("0" + month).slice(-2)
        day = ("0" + day).slice(-2)

        const data_json_path = "./data/day_data/" + year + month + "/day_" + year + month + day + ".json"

        $.when($.getJSON(data_json_path)).then(function (ret) {
            let current_aqi_rader_data_value = project_name.map((val) => {
                return ret[adcode][val]
            })

            let project_name_max = project_limit_max.map((val, index) => {
                return current_aqi_rader_data_value[index] > val ? current_aqi_rader_data_value[index] : val
            })

            let radar_charts01_option = {
                title: {
                    text: adcode_info[adcode].name + ' 空气质量AQI分布图 ' + year + '-' + month + '-' + day,
                    left: 'center',
                    top: 20
                },
                radar: [
                    {
                        indicator: [
                            {text: project_name[0], max: project_name_max[0]},
                            {text: project_name[1], max: project_name_max[1]},
                            {text: project_name[2], max: project_name_max[2]},
                            {text: project_name[3], max: project_name_max[3]},
                            {text: project_name[4], max: project_name_max[4]},
                            {text: project_name[5], max: project_name_max[5]},
                            {text: project_name[6], max: project_name_max[6]},
                        ],
                        center: ['50%', '50%'],
                        radius: 140,
                        axisName: {
                            borderRadius: 3,
                            padding: 5,
                            textBorderType: "solid",
                            textBorderColor: "black",
                            textBorderWidth: 1
                        }
                    }
                ],
                series: [
                    {
                        type: 'radar',
                        radarIndex: 0,
                        data: [
                            {
                                value: current_aqi_rader_data_value,
                                name: '上海市',
                                symbol: 'diamond',
                                symbolSize: 12,
                                lineStyle: {
                                    type: 'solid'
                                },
                                label: {
                                    show: true,
                                    formatter: function (params) {
                                        return params.value;
                                    }
                                }
                            }
                        ]
                    }
                ]
            };

            radar_charts01.setOption(radar_charts01_option);
        })


    }
