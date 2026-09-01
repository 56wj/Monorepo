<template>
    <el-container>
        <!-- <el-aside width="400px" style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1);">
            <el-form ref="form" :model="form" label-width="50px" style="margin-top: 20px;margin-left: 10px;">
                <el-row>
                    <el-col :span=14>
                        <el-form-item label="装箱基本信息：" class="title" label-width="auto"></el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="订单号：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.orderId" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="规则优先级：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.rule" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="混装规则：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.mix" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="横放规则：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.lying" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="最大横放层数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.lying_limit" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="横放托盘：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.lying_tray_flag" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="膜叠膜规则：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.overlap" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="装入卷膜数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.number" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="货物装载信息：" label-width="110px">
                            <el-input type="textarea" v-model="form.info" style="width: 250px;white-space: pre-wrap;word-break: break-all;"
                                :disabled="true" :rows="4"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="装箱剩余货物：" label-width="110px">
                            <el-input type="textarea" v-model="form.residue" style="width: 250px;white-space: pre-wrap;word-break: break-all;"
                                :disabled="true" :rows="4"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="订单卷膜数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.allNumber" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="未装入卷膜数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.residueNumber" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="车箱托盘数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.trayNumber" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="切换车箱：" label-width="110px">
                            <el-select v-model="form.bin" @change="selectBin">
                                <el-option v-for="item in option_bin" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="切换表单：" label-width="110px">
                            <el-button type="primary" @click="showTable = !showTable">{{showTable ? "查看3D图" : "查看详细表单"}}</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item style="display: flex; align-items: center;">
                            <el-button @click="handleConfig">读取配置</el-button>
                        </el-form-item>
                    </el-col>
                    <el-col :span=12>
                        <el-form-item style="display: flex; align-items: center;">
                            <el-button @click="handleExport">导出excel</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
        </el-aside> -->
        <el-aside width="650px" style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1);">
            <el-form ref="form" :model="form" label-width="50px" style="margin-top: 20px;margin-left: 10px;">
                <el-row>
                    <el-col :span=14>
                        <el-form-item label="装箱基本信息：" class="title" label-width="auto"></el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item label="订单号：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.orderId" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span=12>
                        <el-form-item label="规则优先级：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.rule" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item label="混装规则：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.mix" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                     <el-col :span=12>
                        <el-form-item label="横放规则：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.lying" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item label="最大横放层数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.lying_limit" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span=12>
                        <el-form-item label="横放托盘：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.lying_tray_flag" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item label="膜叠膜规则：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.overlap" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span=12>
                        <el-form-item label="装入卷膜数：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.number" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="货物装载信息：" label-width="110px">
                            <el-input type="textarea" v-model="form.info" style="width: 350px;white-space: pre-wrap;word-break: break-all;"
                                :disabled="true" :rows="6"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="装箱剩余货物：" label-width="110px">
                            <el-input type="textarea" v-model="form.residue" style="width: 350px;white-space: pre-wrap;word-break: break-all;"
                                :disabled="true" :rows="6"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="订单卷膜数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.allNumber" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="未装入卷膜数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.residueNumber" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="车箱托盘数：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.trayNumber" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="切换车箱：" label-width="110px">
                            <el-select v-model="form.bin" @change="selectBin">
                                <el-option v-for="item in option_bin" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <!-- <el-row>
                    <el-col :span=16>
                        <el-form-item label="切换表单：" label-width="110px">
                            <el-button type="primary" @click="showTable = !showTable">{{showTable ? "查看3D图" : "查看详细表单"}}</el-button>
                        </el-form-item>
                    </el-col>
                </el-row> -->
                <el-row>
                    <el-col :span=12>
                        <el-form-item style="display: flex; align-items: center;">
                            <el-button @click="handleConfig">读取配置</el-button>
                        </el-form-item>
                    </el-col>
                    <el-col :span=12>
                        <el-form-item style="display: flex; align-items: center;">
                            <el-button @click="handleExport">导出excel</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
        </el-aside>
        <el-container>
            <!-- <el-header style = "border: 1px solid;height: 120px">
                <div>规格信息：</div>
                <el-row><el-cow>剩余货物：</el-cow><el-cow>剩余货物：</el-cow></el-row>
                <div>剩余货物：</div>
            </el-header> -->
            <el-main v-show="!showTable">
                <div id="3D_chart" style="height:100%;width:100%">
                </div>
                <div id="Table" style="height:100%;width:100%;">
                    <!-- <el-table :data="tableData" style="width: 100%;" height=1100px border :summary-method="getSummaries" show-summary> -->
                    <el-table :data="tableData" style="width: 100%;" border :summary-method="getSummaries" show-summary>
                        <el-table-column label="车箱装配表">
                            <!-- <el-table-column label="车箱位置">
                                <el-table-column prop="positionLeft" label="左列" width="50px"></el-table-column>
                                <el-table-column prop="positionRight" label="右列" width="50px"></el-table-column>
                            </el-table-column> -->
                            <el-table-column label="具体内容">
                                <el-table-column label="左列">
                                    <el-table-column prop="positionLeft" label="编号" width="50px"></el-table-column>
                                    <el-table-column prop="thicknessLeft" label="厚度" min-width="18%"></el-table-column>
                                    <el-table-column prop="widthLeft" label="宽度" min-width="24%"></el-table-column>
                                    <el-table-column prop="heightLeft" label="高度" min-width="10%"></el-table-column>
                                    <el-table-column prop="numberLeft" label="数量" min-width="18%"></el-table-column>
                                    <el-table-column prop="weightLeft" label="重量" min-width="18%"></el-table-column>
                                </el-table-column>
                                <el-table-column label="右列">
                                    <el-table-column prop="positionRight" label="编号" width="50px"></el-table-column>
                                    <el-table-column prop="thicknessRight" label="厚度" min-width="18%"></el-table-column>
                                    <el-table-column prop="widthRight" label="宽度" min-width="24%"></el-table-column>
                                    <el-table-column prop="heightRight" label="高度" min-width="10%"></el-table-column>
                                    <el-table-column prop="numberRight" label="数量" min-width="18%"></el-table-column>
                                    <el-table-column prop="weightRight" label="重量" min-width="18%"></el-table-column>
                                </el-table-column>
                            </el-table-column>
                        </el-table-column>
                    </el-table>
                </div>
            </el-main>
            <el-main v-show="showTable">
                <div id="Table" style="height:100%;width:100%;">
                    <!-- <el-table :data="tableData" style="width: 100%;" height=1100px border :summary-method="getSummaries" show-summary> -->
                    <el-table :data="tableData" style="width: 100%;" border :summary-method="getSummaries" show-summary>
                        <el-table-column label="车箱装配表">
                            <!-- <el-table-column label="车箱位置">
                                <el-table-column prop="positionLeft" label="左列" width="50px"></el-table-column>
                                <el-table-column prop="positionRight" label="右列" width="50px"></el-table-column>
                            </el-table-column> -->
                            <el-table-column label="具体内容">
                                <el-table-column label="左列">
                                    <el-table-column prop="positionLeft" label="编号" width="50px"></el-table-column>
                                    <el-table-column prop="thicknessLeft" label="厚度" min-width="18%"></el-table-column>
                                    <el-table-column prop="widthLeft" label="宽度" min-width="24%"></el-table-column>
                                    <el-table-column prop="heightLeft" label="高度" min-width="10%"></el-table-column>
                                    <el-table-column prop="numberLeft" label="数量" min-width="18%"></el-table-column>
                                </el-table-column>
                                <el-table-column label="右列">
                                    <el-table-column prop="positionRight" label="编号" width="50px"></el-table-column>
                                    <el-table-column prop="thicknessRight" label="厚度" min-width="18%"></el-table-column>
                                    <el-table-column prop="widthRight" label="宽度" min-width="24%"></el-table-column>
                                    <el-table-column prop="heightRight" label="高度" min-width="10%"></el-table-column>
                                    <el-table-column prop="numberRight" label="数量" min-width="18%"></el-table-column>
                                </el-table-column>
                            </el-table-column>
                        </el-table-column>
                    </el-table>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { get_result, get_latestTask } from '@/api/task'
import * as echarts from 'echarts'
import 'echarts-gl'
// import { get_latestTask } from '@/api/type1'
import store from '@/store'
import { dataList } from './data'
import { downloadAssetFile, getAssetFileName, getAssetUrl } from '@/utils/asset-url'
export default {
    name: '3D_result',
    data() {
        return {
            form: {
                orderId: "",
                rule: null,
                mix: null,
                overlap: null,
                lying: null,
                lying_limit: null,
                lying_tray_flag: null,
                info: "",
                residue: "",
                taskId: "",
                bin: "",
                number: "",
                allNumber: "",
                residueNumber: "",
                trayNumber: "",
            },
            tableData: [

            ],
            option_bin: [],
            chart_data: {},
            series: [],
            arr: [],
            myChart: '',
            x_label: ['1a', '2a', '3a', '4a', '5a', '6a',
                '7a', '8a', '9a'],
            showTable: false,
            resizeObserver: "",
            source: {},
            bin_height: 300
        }
    },
    created() {console.log("created")},
    methods: {
        to_chart() {
            this.$data.myChart = echarts.init(document.getElementById('3D_chart'));
            this.$data.myChart.on('click', function (params) {
                if(params.value[2] == 0){
                    return
                }
                var i = 2 * params.value[0] + params.value[1]
                var j = "data" + (params.componentIndex+1)
                var detail = that.$data.chart_data[that.$data.form.bin][j]
                // 在新标签页中打开detail的图片连接
                // window.open("http://localhost:9001/"+detail[i].address)
                window.open(getAssetUrl(detail[i].address))
	        });
            var option;
            var that = this;

            var y_label = ['第一列', '第二列'];

            option = {

                // 显示具体信息
                tooltip: {
                    // enterable设置为true，鼠标可进入提示框浮层中
                    enterable: true,
                    // alwaysShowContent一定要设置为true，否则鼠标无法移到tooltip去点击链接
                    alwaysShowContent: true,
                    formatter: function (params) {
                        // console.log(params)
                        var i = 2 * params.value[0] + params.value[1]
                        var j = "data" + (params.componentIndex+1)
                        var detail = that.$data.chart_data[that.$data.form.bin][j]
                        var res = detail[i].name + '<br/>';
                        // res += "<img style='width:180px;height:150px;' src='"+store.getters.url+ "/" + detail[i].address + "'/>";
                        // res+="<a href='"+store.getters.url+"/"+detail[i].address+"' target='_blank'>装箱效果图</a>";
                        // res += "<img style='width:180px;height:150px;' src='http://localhost:9001" + "/" + detail[i].address + "'/>";
                        // res+="<a href='http://localhost:9001" + "/" +detail[i].address + "' target='_blank'>装箱效果图</a>";
                        // res += "<img style='width:180px;height:150px;' src='http://localhost:9527" + "/" + detail[i].address + "'/>";
                        // res+="<a href='http://localhost:9527" + "/" +detail[i].address + "' target='_blank'>装箱效果图</a>";
                        var assetUrl = getAssetUrl(detail[i].address)
                        res += "<img style='width:180px;height:150px;' src='" + assetUrl + "'/>";
                        res+="<a href='" + assetUrl + "' target='_blank'>装箱效果图</a>";
                        // console.log(store.getters.url+"/"+detail[i].address)
                        return detail[i].value[2] != 0 ? res : "顶部";
                    },
                    extraCssText: 'width:200px; white-space:pre-wrap'
                },
                xAxis3D: {
                    type: 'category',
                    data: this.$data.x_label,

                    axisLabel: {
                        show: true,
                        margin: 15,
                        interval: 0,//可控制坐标轴刻度标签的显示间隔，在类目轴中有效。
                    }
                },
                yAxis3D: {
                    type: 'category',
                    data: y_label
                },
                zAxis3D: {
                    type: 'value',
                    max: this.$data.bin_height
                },
                grid3D: {
                    boxWidth: 300,
                    boxDepth: 80,
                    viewControl: {
                        // projection: 'orthographic'
                    },
                    light: {
                        main: {
                            intensity: 1.2,
                            shadow: true
                        },
                        ambient: {
                            intensity: 0.3
                        }
                    }
                },
                series: this.$data.series
            };

            option && this.$data.myChart.setOption(option,true);

        },
        selectBin() {
            this.bin_change();
        },
        bin_change() {
            var bin = this.$data.form.bin;
            var len = Object.keys(this.$data.chart_data[bin]).length;
            this.$data.series = [];
            this.to_chart();
            for (var i = 1; i <= (len - 4); i++) {
                    this.$data.series.push({
                        type: 'bar3D',
                        stack: true,
                        stackStrategy: 'samesign',
                        data: this.$data.chart_data[bin]["data"+ i],
                        shading: 'lambert',
                        itemStyle: {//柱条样式
                            opacity: 0.8,
                        },
                        label: {
                            fontSize: 16,
                            borderWidth: 1
                        },
                        emphasis: {
                            label: {
                                fontSize: 20,
                                color: '#900'
                            },
                            itemStyle: {
                                color: '#900'
                            }
                        }
                    })
            }
            var x_label = [];
            var j = 1;
            this.$data.tableData = [];
            for (i = 1; i <= this.$data.chart_data[bin]["whole_tray_number"] / 2; i++) {
                x_label.push("第" + i + "排")
                // tabledata的更新
                var key1 = "tray" + j++;
                var key2 = "tray" + j++;
                var temp = {
                    thicknessLeft: this.$data.chart_data[bin]["excel_data"][key1]["thickness"],
                    thicknessRight: this.$data.chart_data[bin]["excel_data"][key2]["thickness"],
                    widthLeft: this.$data.chart_data[bin]["excel_data"][key1]["width"],
                    widthRight: this.$data.chart_data[bin]["excel_data"][key2]["width"],
                    heightLeft: this.$data.chart_data[bin]["excel_data"][key1]["total_width"],
                    heightRight: this.$data.chart_data[bin]["excel_data"][key2]["total_width"],
                    numberLeft: this.$data.chart_data[bin]["excel_data"][key1]["number"],
                    numberRight: this.$data.chart_data[bin]["excel_data"][key2]["number"],
                    positionLeft: this.$data.chart_data[bin]["excel_data"][key1]["no"],
                    positionRight: this.$data.chart_data[bin]["excel_data"][key2]["no"],
                    weightLeft: this.$data.chart_data[bin]["excel_data"][key1]["weight"],
                    weightRight: this.$data.chart_data[bin]["excel_data"][key2]["weight"],
                }
                this.$data.tableData.push(temp);
            }
            this.$data.x_label = x_label;
            this.$data.form.info = this.$data.chart_data[bin]["info"];
            this.$data.form.number = this.$data.chart_data[bin]["item_number"];
            this.$data.form.trayNumber = this.$data.chart_data[bin]["tray_number"];
            this.$data.bin_height = this.$data.chart_data[bin]["bin_height"];
            this.to_chart();
        },
        async new_init() {
            if ("obj" in this.$route.query) {
                this.$data.chart_data = JSON.parse(this.$route.query.obj)
                this.$data.arr = Object.keys(this.$data.chart_data)
                // this.$data.source = JSON.parse(this.$route.query.source)
                var config = JSON.parse(this.$route.query.config)
                // var config = this.$data.source.config
                this.$data.form.residue = this.$data.chart_data["residue"]
                this.$data.form.taskId = this.$route.query.taskId
            } else {
                try {
                    const res = await get_latestTask();
                    this.$data.chart_data = res.data.resultJson
                    this.$data.arr = Object.keys(this.$data.chart_data);
                    this.$data.source = res.data.sourceJson
                    var config = res.data.sourceJson.config
                    this.$data.form.residue = this.$data.chart_data["residue"]
                    this.$data.form.taskId = res.data.task.id
                } catch {
                    // this.$message.error("获取数据失败，请刷新页面重试")
                }
            }
            // 车箱单选框初始化
            const regex = /bin/;
            this.$data.option_bin = []
            this.$data.arr.forEach((item, index) => {
                if(regex.test(item)){
                    this.$data.option_bin.push({
                        value: item,
                        label: "车箱" + (index+1) + ": " + this.$data.chart_data[item].bin_name
                    })
                }
            })
            console.log(this.$data.option_bin)
            this.$data.form.allNumber = this.$data.chart_data["all_number"];
            this.$data.form.residueNumber = this.$data.chart_data["residue_item_number"];
            this.$data.form.orderId = config.orderId;
            this.$data.form.bin = this.$data.option_bin[0].value;
            this.$data.form.rule = config.rule == "full" ?  "装满优先" : "平衡优先";
            this.$data.form.mix = config.mix == true ? "允许混装" : "禁止混装";
            this.$data.form.lying = config.lying == true ? "允许横放" : "禁止横放";
            this.$data.form.lying_limit = config.lying_limit;
            this.$data.form.lying_tray_flag = config.lying_tray_flag == true ? "需要托盘" : "无需托盘";
            this.$data.form.overlap = config.overlap == true ? "允许膜叠膜" : "禁止膜叠膜";
            // 增加未装入数显示
            this.bin_change();
        },
        async init() {
            if (Object.keys(this.$route.query).length != 0) {
                this.$data.chart_data = JSON.parse(this.$route.query.obj)
                this.$data.arr = JSON.parse(this.$route.query.arr)
                var config = JSON.parse(this.$route.query.config)
                // console.log(this.$data.chart_data)
                // console.log(this.$data.arr)
                // console.log(config)
            } else {
                const res = await get_latestTask();
                this.$data.chart_data = res.data.resultJson
                this.$data.arr = Object.keys(res.data.resultJson);
                var config = res.data.sourceJson.config;
            }
            for (var i = 0; i < (this.$data.arr.length - 3) / 2; i++) {
                    // console.log(this.$data.arr[i])
                    this.$data.series.push({
                        type: 'bar3D',
                        stack: true,
                        stackStrategy: 'samesign',
                        data: this.$data.chart_data[this.$data.arr[i]],
                        shading: 'lambert',
                        itemStyle: {//柱条样式
                            opacity: 0.8,
                        },
                        label: {
                            fontSize: 16,
                            borderWidth: 1
                        },
                        emphasis: {
                            label: {
                                fontSize: 20,
                                color: '#900'
                            },
                            itemStyle: {
                                color: '#900'
                            }
                        }
                    })
            }
            var x_label = [];
                for (i = 1; i <= this.$data.chart_data["whole_tray_number"] / 2; i++) {
                    x_label.push("第" + i + "排")
                }
            this.$data.x_label = x_label;

            this.$data.form.rule = config.rule == "full" ?  "装满优先" : "平衡优先";
            this.$data.form.mix = config.mix == true ? "允许混装" : "禁止混装";
            this.$data.form.overlap = config.overlap == true ? "允许膜叠膜" : "禁止膜叠膜";
            this.$data.form.info = this.$data.chart_data["info"];
            this.$data.form.residue = this.$data.chart_data["residue"];
            this.to_chart();
        },
        async handleConfig() {
            var data = { taskId: this.$data.form.taskId };
            try {
                const res = await get_result(data);
                console.log(res)
                var source = res.data.sourceJson
                this.$router.push({
                    path: '/type1/get_data',
                    query: {
                        source: source
                    }           
                }) 
            } catch(error) {
                // this.$message.error("读取数据失败，请重试")
            }
        },
        async handleExport() {
            var data = { taskId: this.$data.form.taskId };
            try {
                const res = await get_result(data);
                var url = getAssetUrl(res.data.resultJson.excel_address);
                var fileName = getAssetFileName(res.data.resultJson.excel_address);
                console.log(url)
                console.log(fileName)
                await downloadAssetFile(url, fileName)
                this.$message.success(`结果文件 ${fileName} 已导出`)
            } catch(error) {
                console.error('结果文件导出失败', error)
                this.$message.error(error.message || '结果文件导出失败，请重试')
            }
        },
        getSummaries(param) {
            // 创建一个12项的数组
            const sums = new Array(12).fill("");
            // const { columns, data } = param;
            // 生成合计行所需的数据
            // 数据为chart_data中每个车厢数据的最后一项
            var bin = this.$data.form.bin;
            var index = this.$data.chart_data[bin]["whole_tray_number"];
            var key1 = "tray" + ++index;
            var key2 = "tray" + ++index;
            //  通过chart_data获取数据组成sums
            sums[0] = "合计";
            sums[4] = this.$data.chart_data[bin]["excel_data"][key1]["number"];
            sums[5] = this.$data.chart_data[bin]["excel_data"][key1]["weight"];
            sums[10] = this.$data.chart_data[bin]["excel_data"][key2]["number"];
            sums[11] = this.$data.chart_data[bin]["excel_data"][key2]["weight"];
            return sums;
        },
    },
    mounted() {
        this.new_init();
        this.$data.resizeObserver = new ResizeObserver(() => {
            // 加个if约束，当Echarts存在时再执行resize()，否则图表不存在时运行到这会报错。
            if (this.$data.myChart) {
                this.$data.myChart.resize();
            }

        });
        this.$data.resizeObserver.observe(document.getElementById('3D_chart'));
    },
    activated() {
        this.new_init();
    },
    destroyed() {
        this.$router.push({ query: {redirect: "/type1/3D_result"} })
        this.$data.resizeObserver.unobserve(document.getElementById('3D_chart'))
    }
}
</script>
<style>
.el-header,
.el-footer {
    background-color: #B3C0D1;
    color: #333;
    /* text-align: center; */
    line-height: 60px;
    height: auto;
}

.el-main {
    height: calc(100vh - 50px);
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    /* line-height: 160px; */
}

.el-container {
    height: 100%;
}

.el-aside {
    background-color: #F2F6FC;
    color: #333;
    text-align: center;
    /* line-height: 60px; */
}
</style>
<style lang="scss">
.title .el-form-item__label {
    font-size: 30px;
    align-self: center;
}

.title .el-form-item {
    border-bottom-width: none;
}
.el-input.is-disabled .el-input__inner,textarea:disabled{
  color: #606266 !important;
}
</style>
