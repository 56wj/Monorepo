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
                        <el-form-item label="叠膜规则：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.overlap_way" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="挡板默认厚度：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.baffle_thickness" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="托盘：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.tray" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="膜卷宽度阈值：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.overlap_width" style="width: 200px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=16>
                        <el-form-item label="装箱剩余货物：" label-width="110px">
                            <el-input type="textarea" v-model="form.residue"
                                style="width: 250px;white-space: pre-wrap;word-break: break-all;" :disabled="true"
                                :rows="4"></el-input>
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
                        <el-form-item label="切换车箱：" label-width="110px">
                            <el-select v-model="form.bin" @change="selectBin">
                                <el-option v-for="item in option_bin" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=24>
                        <el-form-item label="切换表单：" label-width="110px">
                            <el-button type="primary"
                                @click="showDetailTable = !showDetailTable, showItemTable = false">{{ showDetailTable ?
                "3D显示" :
                "详细表单" }}</el-button>
                            <el-button type="primary"
                                @click="showItemTable = !showItemTable, showDetailTable = false">{{ showItemTable ?
                "3D显示" :
                "耗材表单" }}</el-button>
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
                        <el-form-item label="叠膜规则：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.overlap_way" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item label="挡板默认厚度：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.baffle_thickness" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span=12>
                        <el-form-item label="膜卷宽度阈值：" label-width="110px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.overlap_width" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=12>
                        <el-form-item label="托盘：" label-width="100px" prop="box_num">
                            <el-input placeholder="请输入" v-model.number="form.tray" style="width: 150px"
                                :disabled="true"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col :span=16>
                        <el-form-item label="装箱剩余货物：" label-width="110px">
                            <el-input type="textarea" v-model="form.residue"
                                style="width: 350px;white-space: pre-wrap;word-break: break-all;" :disabled="true"
                                :rows="6"></el-input>
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
                        <el-form-item label="切换车箱：" label-width="110px">
                            <el-select v-model="form.bin" @change="selectBin">
                                <el-option v-for="item in option_bin" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span=24>
                        <el-form-item label="切换表单：" label-width="110px">
                            <el-button type="primary"
                                @click="showDetailTable = !showDetailTable, showItemTable = false">{{ showDetailTable ?
                "3D显示" :
                "详细表单" }}</el-button>
                            <el-button type="primary"
                                @click="showItemTable = !showItemTable, showDetailTable = false">{{ showItemTable ?
                "3D显示" :
                "耗材表单" }}</el-button>
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
        </el-aside>
        <el-container id="container" style="height:100%;width:100%;">
            <!-- <el-header style = "border: 1px solid;height: 120px">
                <div>规格信息：</div>
                <el-row><el-cow>剩余货物：</el-cow><el-cow>剩余货物：</el-cow></el-row>
                <div>剩余货物：</div>
            </el-header> -->
            <el-main v-show="!showDetailTable && !showItemTable">
                <div id="3D_chart" style="height:100%;width:100%">
                    <!-- <div id="WebGL-output">
                        <div class="css_style" id="lableItem">
                            <span class="css3dTitleWarning" id="lableItemId">00000000000</span>
                        </div>
                    </div> -->
                </div>
            </el-main>
            <el-main v-show="showDetailTable">
                <div id="Table" style="height:100%;width:100%;">
                    <el-container>
                        <el-aside width="550px">
                            <el-form ref="form" :model="form" label-width="50px"
                                style="margin-top: 20px;margin-left: 10px;">
                                <el-row>
                                    <el-col :span=14>
                                        <el-form-item label="俯视图：" class="title" label-width="auto"></el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col :span=24>
                                        <img :src="pictureUrl" style="width: 100%;">
                                    </el-col>
                                </el-row>
                            </el-form>
                        </el-aside>
                        <el-main> 
                            <el-table :data="detailTableData" border style="height:100%;width: 100%;" :max-height="maxHeight">
                                <el-table-column prop="id" label="编号" width="50">
                                </el-table-column>
                                <el-table-column prop="name" label="货物内容" width="150">
                                </el-table-column>
                                <el-table-column prop="d" label="直径" width="80">
                                </el-table-column>
                                <el-table-column label="木托">
                                    <el-table-column prop="tray_size" label="规格"></el-table-column>
                                    <el-table-column prop="tray_number" label="数目"></el-table-column>
                                </el-table-column>
                                <el-table-column label="挡板">
                                    <el-table-column prop="baffle_size" label="规格"></el-table-column>
                                    <el-table-column prop="baffle_number" label="数目"></el-table-column>
                                </el-table-column>
                            </el-table>
                        </el-main>
                    </el-container>
                </div>
            </el-main>
            <el-main v-show="showItemTable">
                <div id="Table" style="height:100%;width:100%;">
                    <el-table :data="itemTableData" border style="width: 100%">
                        <el-table-column prop="name" label="品名" width="240">
                        </el-table-column>
                        <el-table-column prop="size" label="规格" width="240">
                        </el-table-column>
                        <el-table-column prop="unit" label="单位" width="240">
                        </el-table-column>
                        <el-table-column prop="number" label="数量" width="240">
                        </el-table-column>
                        <el-table-column prop="date" label="到货日期" width="240">
                        </el-table-column>
                        <el-table-column prop="rotation" label="备注">
                        </el-table-column>
                    </el-table>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import { mapGetters } from 'vuex'
import store from '@/store'
import { get_result, get_latestTask2 } from '@/api/task'
import { mockData } from './mockData'
import { realData } from './realData'
// import { PackagePreview3DInit } from '@/3D/pallet'
import { PackagePreview3DInit } from '@/3D/pallet2'
import { downloadAssetFile, getAssetFileName, getAssetUrl } from '@/utils/asset-url'
export default {
    name: '3D_result2',
    data() {
        return {
            form: {
                orderId: "",
                overlap_way: "",
                baffle_thickness: "",
                tray: "",
                overlap_width: "",
                residue: "",
                taskId: "",
                bin: "",
                number: "",
                allNumber: "",
                residueNumber: "",
                trayNumber: "",
            },
            tableData: [],
            option_bin: [],
            showDetailTable: false,
            showItemTable: false,
            detailTableData: [],
            itemTableData: [],
            pictureUrl: "",
            maxHeight: window.innerHeight-100,
        }
    },
    // created() { this.$data.tableData = realData.singleContainerLoadingSolutions },
    methods: {
        test() {
            console.log("sss");
            PackagePreview3DInit(this.$data.chart_data);
        },
        selectBin() {
            this.bin_change();
        },
        bin_change() {
            var bin = this.$data.form.bin;
            this.$data.pictureUrl = getAssetUrl(this.$data.chart_data[bin]["picture_address"]);
            // this.$data.form.number = this.$data.chart_data[bin]["item_number"];
            // this.$data.form.trayNumber = this.$data.chart_data[bin]["tray_number"];
            // this.$data.bin_height = this.$data.chart_data[bin]["bin_height"];
            this.$data.detailTableData = this.$data.chart_data[bin]["placed_items"];
            PackagePreview3DInit(this.$data.chart_data[bin]);
        },
        async new_init() {
            console.log("new_init")
            if ("data" in this.$route.query) {
                this.$data.chart_data = JSON.parse(this.$route.query.data)
                this.$data.arr = Object.keys(this.$data.chart_data)
                var config = JSON.parse(this.$route.query.config)
                // this.$data.form.residue = this.$data.chart_data["residue"]
                this.$data.form.taskId = this.$route.query.taskId
                console.log(this.$data.chart_data)
                console.log(this.$data.arr)
                console.log(config)
                // this.test();
            } else {
                try {
                    const res = await get_latestTask2();
                    this.$data.chart_data = res.data.resultJson
                    this.$data.arr = Object.keys(this.$data.chart_data);
                    var config = res.data.sourceJson.config
                    // this.$data.form.residue = this.$data.chart_data["residue"]
                    this.$data.form.taskId = res.data.task.id
                } catch {
                    // this.$message.error("获取数据失败，请刷新页面重试")
                }
            }
            // 车箱单选框初始化
            const regex = /bin/;
            this.$data.option_bin = []
            this.$data.arr.forEach((item, index) => {
                if (regex.test(item)) {
                    this.$data.option_bin.push({
                        value: item,
                        // label: "车箱" + (index+1) + ": " + this.$data.chart_data[item].bin_name
                        label: "车箱" + (index + 1)
                    })
                }
            })
            console.log(this.$data.option_bin)
            // this.$data.form.allNumber = this.$data.chart_data["all_number"];
            // this.$data.form.residueNumber = this.$data.chart_data["residue_item_number"];
            this.$data.itemTableData = this.$data.chart_data["excel_data"];
            this.$data.form.orderId = config.orderId;
            this.$data.form.bin = this.$data.option_bin[0].value;
            this.$data.form.overlap_way = config.overlap_way;
            this.$data.form.baffle_thickness = config.baffle_thickness;
            this.$data.form.tray = config.tray;
            this.$data.form.overlap_width = config.overlap_width;
            this.$data.form.residue = this.$data.chart_data["remain_items"];
            this.$data.form.allNumber = this.$data.chart_data["all_number"];
            this.$data.form.residueNumber = this.$data.chart_data["remain_items_count"];
            // 增加未装入数显示
            this.bin_change();
        },
        async handleConfig() {
            var data = { taskId: this.$data.form.taskId };
            try {
                const res = await get_result(data);
                console.log(res)
                var source = res.data.sourceJson
                this.$router.push({
                    path: '/type2/get_data2',
                    query: {
                        source: source
                    }
                })
            } catch (error) {
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
            } catch (error) {
                console.error('结果文件导出失败', error)
                this.$message.error(error.message || '结果文件导出失败，请重试')
            }
        },
    },
    mounted() {
        this.new_init();
        window.addEventListener("resize", () => {
            this.$data.maxHeight = window.innerHeight-100;
        });
    },
    activated() {
        console.log("3D2 activated")
        this.new_init();
    },
    destroyed() { console.log("destroyed") },
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

.el-input.is-disabled .el-input__inner,
textarea:disabled {
    color: #606266 !important;
}

.css_style {
    background-color: MidnightBlue;
    background-color: rgba(0, 10, 40);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    opacity: 0.5;
    font-size: 4px;
    color: aqua;
    padding: 10px 10px 10px;
    white-space: nowrap;
    width: 200px;
    height: 80px;
    font-size: medium;
}

#lableItemId {
    display: inline-block;
    white-space: normal;
    word-wrap: break-word;
    word-break: break-all;
    max-width: 180px;
}


.css_style:after {
    content: "";
    border-style: solid;
    border-top: 18px solid rgba(0, 10, 40);
    ;
    border-right: 8px solid transparent;
    border-bottom: 18px solid transparent;
    border-left: 8px solid transparent;
    /* border-left: 18px solid rgba(0, 10, 40); */
    ;
    position: absolute;
    left: 50%;
    top: 100%;
    /* margin-top: 18px; */
    margin-right: 18px;
}
</style>
