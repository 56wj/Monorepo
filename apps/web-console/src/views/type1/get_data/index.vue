<!-- npm run dev  npm run build:prod -->
<template>
  <div class="dashboard-container">
    <el-form ref="form" :model="form" :rules="rules" label-width="100px">
      <el-tabs v-model="activeName" @tab-click="" style="box-shadow: 6px 6px 6px rgba(0,0,0,0.1); height: 900px;">
        <el-tab-pane label="规则设置" name="first">
          <el-divider content-position="left">通用设置</el-divider>
          <el-row style="margin-top: 20px">
            <el-col :span=12>
              <el-form-item label="总规则：" label-width="220px">
                <el-select v-model="form.rule">
                  <el-option v-for="item in options_rule" :key="item.value" :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="订单号：" label-width="220px" prop="orderId">
                <el-input placeholder="请输入" v-model="form.orderId" style="width: 250px" clearable>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span=12>
              <el-form-item label="托盘规则：" label-width="220px">
                <el-select v-model="form.tray_rule" @change="traySize">
                  <el-option v-for="item in options_tray_rule" :key="item.value" :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="托盘尺寸：" label-width="220px">
                <el-select v-model="form.tray_size" :disabled="form.tray_rule!='human'">
                  <el-option v-for="item in options_tray_size" :key="item.value" :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span=12>
              <el-form-item label="允许超出托盘长度范围(cm)：" label-width="220px" prop="beyond_height">
                <el-input placeholder="请输入" v-model.number="form.beyond_height" style="width: 250px" clearable>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="允许超出托盘宽度范围(cm)：" label-width="220px" prop="beyond_width">
                <el-input placeholder="请输入" v-model.number="form.beyond_width" style="width: 250px" clearable>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span=12>
              <el-form-item label="泡沫高度设置(cm)：" label-width="220px" prop="froth_height">
                <el-input placeholder="请输入" v-model.number="form.froth_height" style="width: 250px" clearable>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="纸管尺寸：" label-width="220px">
                <el-select v-model="form.tubeId" @change="get_diameter">
                  <el-option v-for="item in options_tube" :key="item.value" :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span=12>
              <el-form-item label="可否混装：" label-width="220px">
                <!-- 如果需要绑定数值或者布尔类型的值，需要在label前加上: -->
                <el-radio v-model="form.mix" :label="true" border>允许混装</el-radio>
                <el-radio v-model="form.mix" :label="false" border>禁止混装</el-radio>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="默认密度：" label-width="220px">
                <el-input placeholder="请输入" v-model="form.default_density" @input="exitCheck_density(form.default_density)" @blur="exitSave_density(form.default_density)" style="width: 250px" clearable>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-divider content-position="left">横放设置</el-divider>
          <el-row>
            <el-col :span=12>
              <el-form-item label="可否横放：" label-width="220px">
                <el-radio-group v-model="form.lying" @change="lying">
                  <el-radio :label="true" border>允许横放</el-radio>
                  <el-radio :label="false" border>禁止横放</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="最大横放层数限制：" key="3" label-width="220px" prop="lying_limit">
                <el-input placeholder="请输入" v-model.number="form.lying_limit" style="width: 250px" clearable
                  :disabled="!form.lying">
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span=12>
              <el-form-item label="横放是否需要托盘：" label-width="220px">
                <el-radio-group v-model="form.lying_tray_flag">
                  <el-radio :label="true" border>需要托盘</el-radio>
                  <el-radio :label="false" border>无需托盘</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span=12>
              <el-form-item label="算法参数x(cm)：" label-width="220px" prop="parmX">
                <el-input placeholder="请输入" v-model.number="form.parmX" style="width: 250px" clearable>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-divider content-position="left">叠膜设置</el-divider>
          <el-alert
            class="overlap-rule-tip"
            title="高度统一填 cm：规格宽度780mm按78cm判断，700mm按70cm判断"
            description="“单层上限”只决定该规格能否参与叠膜；实际叠膜还要满足同规格、非混装小托且叠后膜卷本体总高度不超过“总高度上限”。两个上限均不含托盘和泡沫高度。"
            type="info"
            :closable="false"
            show-icon>
          </el-alert>
          <el-row>
            <el-col :span=12>
              <el-form-item label="可否膜叠膜：" label-width="220px">
                <el-radio-group v-model="form.overlap" @change="overlap">
                  <el-radio :label="true" border>允许膜叠膜</el-radio>
                  <el-radio :label="false" border>禁止膜叠膜</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <!-- <el-col :span=12>
              <el-form-item label="可否混装：" label-width="220px">
                <el-radio v-model="form.mix" :label="true" border>允许混装</el-radio>
                <el-radio v-model="form.mix" :label="false" border>禁止混装</el-radio>
              </el-form-item>
            </el-col> -->
          </el-row>
          <el-row>
            <el-col :span=12>
              <el-form-item label="单层膜卷本体高度上限(cm)：" key="1" label-width="270px" prop="single_max_height">
                <el-input placeholder="例如 70（等于700mm）" v-model.number="form.single_max_height" style="width: 250px" clearable
                  :disabled="!form.overlap">
                </el-input>
                <span v-if="form.overlap && heightCmToMm(form.single_max_height) !== null" class="height-conversion-tip">
                  = {{ heightCmToMm(form.single_max_height) }} mm
                </span>
              </el-form-item>
              <!-- <el-form-item label="单个膜叠膜最大高度(cm)：" key="2" v-else label-width="220px" prop="single_max_height">
                <el-input placeholder="请输入" v-model.number="form.single_max_height" style="width: 250px" clearable>
                </el-input>
              </el-form-item> -->
            </el-col>
            <el-col :span=12>
              <el-form-item label="叠后膜卷本体总高度上限(cm)：" key="1" label-width="270px" prop="entire_max_height">
                <el-input placeholder="例如 140（等于1400mm）" v-model.number="form.entire_max_height" style="width: 250px" clearable
                  :disabled="!form.overlap">
                </el-input>
                <span v-if="form.overlap && heightCmToMm(form.entire_max_height) !== null" class="height-conversion-tip">
                  = {{ heightCmToMm(form.entire_max_height) }} mm
                </span>
              </el-form-item>
              <!-- <el-form-item label="总体膜叠膜最大高度(cm)：" key="2" v-else label-width="220px" prop="entire_max_height">
                <el-input placeholder="请输入" v-model.number="form.entire_max_height" style="width: 250px" clearable>
                </el-input>
              </el-form-item> -->
            </el-col>
          </el-row>

        </el-tab-pane>
        <el-tab-pane label="车箱配置" name="second">
          <el-table :data="form.box_list" style="width: 100%; margin-top: 20px" height=530px border>
            <el-table-column prop="box_id" label="车箱" width="240">
              <template slot-scope="scope">
                <el-select v-model="scope.row.box_id">
                    <el-option v-for="item in options_box_type" :key="item.value" :label="item.label"
                      :value="item.value">
                    </el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="num" label="数量" width="240">
              <template slot-scope="scope">
                <el-input-number v-model="scope.row.num" :min="1" :max="10"></el-input-number>
              </template>
            </el-table-column>
            <el-table-column prop="box_id" label="规格">
              <template slot-scope="scope">
                <el-select v-model="scope.row.box_id" disabled style="width: 400px;">
                    <el-option v-for="item in options_box_detail" :key="item.value" :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
              </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="200">
              <template slot="header" slot-scope="scope">
                <el-button @click="addBox2">新增车箱</el-button>
              </template>
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="removeBox2(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="数据导入" name="third" class="three">
          <el-row>
            <el-col :span=8>
              <el-form-item label="重量单位：">
                <el-switch
                  v-model="form.t_or_kg"
                  active-text="kg"
                  inactive-text="T">
                </el-switch>
              </el-form-item>
            </el-col>
            <el-col :span=16 class="data-import-actions">
              <el-upload class="filter-item" name="file" action="string" :on-error="uploadFalse"
                :on-success="uploadSuccess" :on-change="get_content" :before-upload="beforeAvatarUpload"
                ref="upload" accept=".xlsx,.xls" :show-file-list="false" :file-list="fileList"
                :http-request="uploadData" :auto-upload="false">
                <el-button slot="trigger" icon="el-icon-upload2" type="primary">货物数据上传</el-button>
              </el-upload>
              <el-button icon="el-icon-download" @click="historyExportVisible = true">历史订单导出</el-button>
            </el-col>
          </el-row>
          <el-table :data="pageData" style="width: 100%;" height=530px>
            <el-table-column prop="name" label="品名" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.name" placeholder="请输入内容"></el-input>
                <div v-else class="txt">{{ scope.row.name }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="order_thickness" label="订单厚度" width="180">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.order_thickness"
                  placeholder="请输入内容" @input="exitCheck('order_thickness', scope.row)" @blur="exitSave('order_thickness', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.order_thickness }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="real_thickness" label="厚度" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.real_thickness"
                  placeholder="请输入内容" @input="exitCheck('real_thickness', scope.row)" @blur="exitSave('real_thickness', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.real_thickness }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="width" label="宽度" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.width" placeholder="请输入内容"
                @input="exitCheck('width', scope.row)" @blur="exitSave('width', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.width }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="order_height" label="订单长度" width="180">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.order_height"
                  placeholder="请输入内容" @input="exitCheck('order_height', scope.row)" @blur="exitSave('order_height', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.order_height }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="real_height" label="长度" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.real_height"
                  placeholder="请输入内容" @input="exitCheck('real_height', scope.row)" @blur="exitSave('real_height', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.real_height }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="number" label="卷数" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.number"
                  placeholder="请输入内容"></el-input>
                <div v-else class="txt">{{ scope.row.number }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="density" label="密度" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.density"
                  placeholder="请输入内容" @input="exitCheck('density', scope.row)" @blur="exitSave('density', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.density }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="weight" label="重量" width="240">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.weight"
                  placeholder="请输入内容" @input="exitCheck('weight', scope.row)" @blur="exitSave('weight', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.weight }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="diameter" label="直径">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model="scope.row.diameter"
                  placeholder="请输入内容" @input="exitCheck('diameter', scope.row)" @blur="exitSave('diameter', scope.row)"></el-input>
                <div v-else class="txt">{{ scope.row.diameter }}</div>
              </template>
            </el-table-column>
            <!-- <el-table-column prop="priority" label="优先级">
              <template slot-scope="scope">
                <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.priority"
                  placeholder="请输入内容"></el-input>
                <div v-else class="txt">{{ scope.row.priority }}</div>
              </template>
            </el-table-column> -->
            <el-table-column fixed="right" label="操作" width="200">
              <template slot-scope="scope">
                <el-button size="mini" v-if="scope.row.isEdit"
                  @click="handleSave(scope.$index, scope.row)">保存</el-button>
                <el-button size="mini" v-else @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <!--分页-->
          <el-row>
            <el-col style="text-align:center">
              <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                :current-page="currentpage" :page-sizes="[10, 20, 30]" :page-size="pagesize"
                layout="total, sizes, prev, pager, next, jumper" :total="total">
              </el-pagination>
            </el-col>
          </el-row>
        </el-tab-pane>
        <div style="display: flex; justify-content: center;">
          <el-form-item label-width="0px">
            <el-button type="success" @click="uploadData" :loading="loading" :disabled="wsp">{{ loading ?
      '计算中 ...'
      : '开始计算'
              }}</el-button>
          </el-form-item>
        </div>
      </el-tabs>
    </el-form>
    <el-dialog title="规格确认表" :visible.sync="dialogTableVisible" :before-close="handleClose">
      <el-table :data="dialog" :key="forceRefresh" height=530px border>
        <el-table-column property="item_hd" label="厚度" width="200"></el-table-column>
        <el-table-column property="item_cd" label="长度" width="200"></el-table-column>
        <el-table-column property="often_number" label="规格表个数" width="200">
          <template slot-scope="scope">
            <el-input v-if="scope.row.isEdit2" class="item" v-model.number="scope.row.often_number" placeholder="请输入盛放个数"></el-input>
            <div v-else class="txt">{{ tray1111(scope.row) }}</div>
          </template>
        </el-table-column>
        <el-table-column property="number" label="单托盘可放个数">
          <template slot-scope="scope">
            <el-input v-if="scope.row.isEdit" class="item" v-model.number="scope.row.number" placeholder="请输入盛放个数"></el-input>
            <div v-else class="txt">{{ scope.row.number }}</div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" v-if="scope.row.isEdit"
            @click="handleSave2(scope.$index, scope.row)">保存</el-button>
            <el-button size="mini" v-else @click="handleEdit2(scope.$index, scope.row)" :disabled="oneEdit2">编辑</el-button>
            <el-button size="mini" v-if="scope.row.isEdit2"
            @click="handleCreate2(scope.$index, scope.row)">确认</el-button>
            <el-button size="mini" v-else @click="handleCreate(scope.$index, scope.row)" :disabled="!scope.row.isNull">创建</el-button>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog">取 消</el-button>
        <el-button type="primary" @click="submitDialog" :loading="loading2" :disabled="oneEdit2">{{ loading2 ? '计算中' : '确定' }}</el-button>
      </span>
    </el-dialog>
    <historical-order-export-dialog
      :visible.sync="historyExportVisible"
      task-type="托盘装箱"
    />
  </div>
</template>

<script>
import { post_file, post_al_first,post_al_second } from '@/api/type1'
import { check, save } from '@/utils/inputCheck'
import { get_box } from '@/api/box'
import { get_pallet } from '@/api/pallet'
import { get_tube } from '@/api/tube'
import { mapGetters } from 'vuex'
import * as xlsx from 'xlsx/xlsx.mjs'
import { getToken } from '@/utils/auth'
import { palletDataCheck }from '@/utils/inputCheck'
import { create_palletroll } from '@/api/rollPallet'
import { get_task } from '@/api/external'
import { heightCmToMm, validateOverlapConfig, validateOverlapHeightValue } from '@/utils/overlapValidation'
import HistoricalOrderExportDialog from '@/components/HistoricalOrderExportDialog'
import ReconnectingWebSocket, { buildWebSocketUrl } from '@/utils/reconnectingWebSocket'


export default {
  name: 'get_data',
  components: { HistoricalOrderExportDialog },
  data() {
    const overlapHeightValidator = (fieldLabel) => (rule, value, callback) => {
      if (!this.form.overlap) {
        callback()
        return
      }
      const message = validateOverlapHeightValue(value, fieldLabel)
      message ? callback(new Error(message)) : callback()
    }
    return {
      activeName: 'first',
      form: {
        rule: 'full',
        mix: true,
        tray_rule: 'computer',
        tray_size: '1.1*1.1',
        lying: false,
        lying_limit: 4,
        lying_tray_flag: false,
        overlap: false,
        single_max_height: '',
        entire_max_height: '',
        beyond_height: 0,
        beyond_width: 0,
        froth_height: 5,
        default_density: 0.905,
        parmX: 110,
        orderId: '',
        box_list: [{
          box_id: '',
          num: 1
        }],
        tubeId: '',
        t_or_kg: false,
      },
      rules: {
        orderId: [
          { required: true, message: '请输入订单号', trigger: 'blur' },
          // 更新正则表达式，匹配字母和数字和-
          { pattern: /^[a-zA-Z0-9-]+$/, message: '订单号只能包含字母、数字和-', trigger: 'blur' }
          // { pattern: /^-?\d+(-?\d+)*$/, message: '请输入正确数据', trigger: 'blur' }
          // { len: 6, message: '请输入6位订单号', trigger: 'blur' }
        ],
        single_max_height: [
          { validator: overlapHeightValidator('单层膜卷本体高度上限'), trigger: ['blur', 'change'] }
        ],
        entire_max_height: [
          { validator: overlapHeightValidator('叠后膜卷本体总高度上限'), trigger: ['blur', 'change'] }
        ],
        beyond_height: [
          { required: true, message: '请输入高度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        beyond_width: [
          { required: true, message: '请输入宽度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        froth_height: [
          { required: true, message: '请输入高度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        parmX: [
          { required: true, message: '请输入参数(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        box_num: [
          { required: true, message: '请输入长度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        box_length: [
          { required: true, message: '请输入长度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        box_height: [
          { required: true, message: '请输入高度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        box_width: [
          { required: true, message: '请输入宽度(cm)', trigger: 'blur' },
          { type: 'number', message: '高度必须为数字值' }
        ],
        lying_limit: [
          { required: true, message: '请输入层数', trigger: 'blur' },
          { type: 'number', message: '层数必须为数字值' }
        ]
      },
      options_rule: [{
        value: 'full',
        label: '装满优先'
      }, {
        value: 'balance',
        label: '平衡优先'
      }],
      options_tray_rule: [{
        value: 'computer',
        label: '程序指定'
      }, {
        value: 'human',
        label: '人工指定'
      }],
      options_tray_size: [],
      options_box_type: [],
      options_box_detail: [],
      options_tube: [],
      fileList: [],
      xlsxData: [],
      tableData: [],
      total: 0,  //总数据条数
      currentpage: 1,  //当前所在页默认是第一页
      pagesize: 10,  //每页显示多少行数据 默认设置为10
      pageData: [],//分页后的当前页数据
      tube: [],
      loading: false,
      loading2: false,
      show_tray: true,
      input_overlap: true,
      input_lying: true,
      dialogTableVisible: false,
      wsp: false,
      oneEdit2: false,
      dialogTempNum: 0,
      forceRefresh: "",
      ws: "",
      box_id: '',
      box_height: '',
      box_max_height: '',
      taskId: '',
      dialog: [],
      trayId: '',
      historyExportVisible: false
    }
  },
  methods: {
    heightCmToMm,
    async init() {
      try {
        const res = await get_box()
        const res2 = await get_pallet()
        const res3 = await get_tube()
        // console.log(res2)
        res.data.forEach((item) => {
          this.options_box_type.push({
            value: item.id,
            label: item.name,
            height: item.heightM
          })
          this.options_box_detail.push({
            value: item.id,
            label: "长度(m)" + item.lengthM + "  " + "宽度(m)" + item.widthM + "  " + "高度(m)" + item.heightM + "  " + "载重(t)" + item.weightT
          })
        })
        res2.data.forEach((item) => {
          this.options_tray_size.push({
            value: item.id,
            label: item.palletName
          })
        })
        res3.data.forEach((item) => {
          this.options_tube.push({
            value: item.id,
            label: item.tubeName+"("+item.tubeApproximate+")"
          })
          this.tube.push({
            id: item.id,
            value: item.tubeApproximate
          })
        })

        this.$data.box_id = res.data[0].id
        // this.$data.box_height = res.data[0].heightM

        if ("source" in this.$route.query && this.$route.query.source.config != null){
          this.$data.form = this.$route.query.source.config
          this.$data.tableData = this.$route.query.source.tableData
          this.getPageInfo()
        }else{
          this.$data.form.box_list[0].box_id = this.$data.box_id
          this.$data.form.tray_size = res2.data[0].id
          this.$data.form.tubeId = res2.data[0].id
          if("push_id" in this.$route.query && this.$route.query.push_id != null){
            var data = { pushId: this.$route.query.push_id }
            const res4 = await get_task(data)
            this.$data.form.orderId = res4.data.orderId
            this.$data.tableData = res4.data.orderData.tableData
            this.push_get_density()
            this.get_diameter()
            this.get_weights()
            this.getPageInfo()
          }
        }

        // this.getBoxHeight()
      } catch (error) {
        // this.$message.error("获取车箱数据失败，请刷新页面")
      }
    },
    submitUpload() {
      this.$refs.upload.submit();
    }, 
    async uploadFile(param) {
      const File = param.file;
      let formData = new FormData();
      formData.append("file", File);
      // 文件上传
      // this.loading = true
      const res = await post_file(formData)
      // 上传成功 （创建websocket）
      console.log(res)
      // 上传失败
    },
    uploadData(param) {
      this.$refs['form'].validate((valid) => {
        if(!valid){
          this.activeName = 'first'
          this.$message.error("规则设置有误，请检查红色提示项")
        }else if(palletDataCheck(this.$data.tableData)&&this.logicCheck()){
          console.log('submit!');
          this.to_upload();
        }
        // if (valid&&palletDataCheck(this.$data.tableData)) {
        //   console.log('submit!');
        //   this.to_upload();
        // } else {
        //   console.log('error submit!!');
        //   alert("输入有误，请检查！");
        //   return false;
        // }
      });
    },
    async to_upload(){
      this.$data.loading = true;
        this.$message({
              message: "开始计算，请勿离开当前页面！",
              type: 'success',
              duration: 5 * 1000
            })
        var data = {
          orderID: this.$data.form.orderId,
          data: {
            config: this.$data.form,
            tableData: this.$data.tableData
          }
        };
        if(this.$data.form.t_or_kg){
          data.data.tableData.forEach((item2)=>{
            item2.weight/=1000;
          })
        }
        try {
          const res = await post_al_first(data);
          console.log(res)
          this.$data.taskId = res.data;
        } catch (error) {
          this.$data.loading = false;
          console.log(error)
          this.$message.error("一阶段提交失败，请重新提交")
        }
    },
    async uploadSuccess(response, file, fileList) {
      console.log("response")
      this.$refs.upload.clearFiles();
      // console.log(response)
      //   if (response.status==20000) {
      //     this.$message({
      //       message: response.message,
      //       type: 'success'
      //     });
      //   } else {
      //     this.$message({
      //       message: response.message,
      //       type: 'error'
      //     });
      //   }
      // this.$refs.upload.clearFiles(); //上传成功之后清除历史记录
    },
    uploadFalse(response, file, fileList) {
      this.$message({
        message: '文件上传失败！',
        type: 'error'
      });
      this.$refs.upload.clearFiles();
    },
    // 上传前对文件的大小的判断
    beforeAvatarUpload(file) {
      // console.log(file)
      const extension = file.name.split(".")[1] === "xls";
      const extension2 = file.name.split(".")[1] === "xlsx";
      const isLt2M = file.size / 1024 / 1024 < 10;
      if (!extension && !extension2) {
        this.$message({
          message: '上传模板只能是 xls、xlsx格式!',
          type: 'error'
        }); c
      }
      if (!isLt2M) {
        console.log("上传模板大小不能超过 10MB!");
        this.$message({
          message: '上传模板大小不能超过 10MB!',
          type: 'error'
        });
      }
      return extension || extension2 || extension3 || (extension4 && isLt2M);
    },
    get_content(file, fileList) {
      if (fileList.length > 1) {
        console.log(1)
        fileList.splice(0, 1);
     }
     console.log(2)
      if (!file.name) { // 如果没有文件名
        return false
      } else if (!/\.(xls|xlsx)$/.test(file.name.toLowerCase())) {
        this.$message.error('上传格式不正确，请上传xls或者xlsx格式')
        return false
      }

      const fileReader = new FileReader()
      fileReader.onload = (files) => {
        try {
          const data = files.target.result
          const workbook = xlsx.read(data, {
            type: 'binary'
          })
          const wsname = workbook.SheetNames[0]// 取第一张表
          const ws = xlsx.utils.sheet_to_json(workbook.Sheets[wsname])// 生成json表格内容
          // console.log(ws, 'ws是表格里的数据，且是json格式')
          this.$data.xlsxData = ws
          // console.log(this.$data.xlsxData[0].品名)
          this.get_tableData()
          // 重写数据
          this.$refs.upload.value = ''
          // return ws
        } catch (e) {
          console.log(e)
          return false
        }
      }
      fileReader.readAsBinaryString(file.raw)
    },
    diameter(f,c){
      // 如果f和c不合法或为空，返回0
      if (f == null || f <= 0 || c == null || c <= 0) {
        return 0;
      }
      const tube_diameter = this.tube.find(item => item.id == this.$data.form.tubeId).value
      return Math.sqrt(4*f*(c+0.7)/3.14+tube_diameter)
      // return Math.sqrt(4*f*(c+0.7)/3.14+9216)
    },
    get_diameter(){
      if(this.$data.tableData.length == 0){
        return
      }
      this.$data.tableData.forEach((item)=>{
        item.diameter = this.diameter(item.real_height, item.real_thickness)
      })
    },
    get_weight(f, c, l, d, n, w){
      /* 膜卷重量=厚度*宽度*长度*密度/1000000000*卷数，
      需要加列密度在导入件格式中，如果导入件或通过接口获取的数据有重量的，
      则两者比较重量差异在5%范围内的按导入件或接口获取重量为准，超出范围的按计算重量为准。
      */
     // 如果f、c、l、d、n不合法或为空，返回0
     d = save(d)
    //  console.log(d)
      if (f == null || f <= 0 || c == null || c <= 0 || l == null || l <= 0 || d == null || d <= 0 || n == null || n <= 0) {
        return 0;
      }
      const weight = f * c * l * d * n / (1000000000);
      if (w != null && w != '' && w != 0) {
        if(this.$data.form.t_or_kg){
          w /= 1000; // 如果是kg单位，则转换为t
        }
        const diff = Math.abs(weight - w) / w;
        if (diff <= 0.05) {
          return w; // 返回导入件或接口获取的重量
        }
      }
      return weight;
    },
    get_weights() {
      if(this.$data.tableData.length == 0){
        return
      }
      this.$data.tableData.forEach((item)=>{
        item.weight = this.get_weight(item.real_height, item.real_thickness, item.width, item.density, item.number, item.weight)
      })
    },
    push_get_density() {
      if(this.$data.tableData.length == 0){
        return
      }
      this.$data.tableData.forEach((item)=>{
        item.density = this.$data.form.default_density
      })
    },
    get_tableData() {
      const that = this
      const obj = {
        品名: 'name',
        订单厚度: 'order_thickness',
        厚度: 'real_thickness',
        宽度: 'width',
        订单长度: 'order_height',
        长度: 'real_height',
        卷数: 'number',
        密度: 'density',
        重量: 'weight',
        直径: 'diameter',
        优先级: 'priority'
      }
      var arr = []
      //2：通过数组循环转换产生一个新的数组（key值为英文）
      this.$data.xlsxData.forEach((res) => {
        const newObj = { isEdit: false }
        // 判断改行是否为空
        if (!this.isEmptyOrWhitespaceOnly(Object.values(res))) {
          Object.keys(res).forEach((item2) => {
            // 赋值英文key与值到新对象
            if (item2 != '__EMPTY') { newObj[obj[item2]] = res[item2] }
          })
          if(!('diameter' in newObj)){
            newObj['diameter'] = that.diameter(newObj['real_height'], newObj['real_thickness'])
          }
          if(!('priority' in newObj)){
            newObj['priority'] = 1
          }
          if(!('density' in newObj)){
            newObj['density'] = that.$data.form.default_density
          }
          arr.push(newObj)
        }
      })
      // console.log(arr)
      // if(this.$data.form.t_or_kg){
      //   arr.forEach((item)=>{
      //     item.weight/=1000;
      //   })
      // }
      // console.log(arr)
      this.$data.tableData = arr
      // this.$data.total = arr.length
      this.get_weights()
      this.getPageInfo()
    },
    isEmptyOrWhitespaceOnly(row) {
    // 检查每个单元格是否为空或只包含空格
    return row.every(cell => typeof cell === 'string' && !cell.trim());
    },
    //修改、删除数据，以及保存、编辑的按钮切换
    handleEdit(index, row) {
      var id = (this.$data.currentpage - 1) * this.$data.pagesize;
      row.isEdit = true;
    },
    handleSave(index, row) {
      row.isEdit = false;
      row.diameter = this.diameter(row.real_height, row.real_thickness)
      row.weight = this.get_weight(row.real_height, row.real_thickness, row.width, row.density, row.number, row.weight)
      // console.log(row)
    },
    handleDelete(index, row) {
      // var id = (this.$data.currentpage - 1) * this.$data.pagesize + index;
      // this.$data.tableData.splice(id, 1);
      // this.getPageInfo();
      this.$confirm('将删除本条数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        var id = (this.$data.currentpage - 1) * this.$data.pagesize + index;
        this.$data.tableData.splice(id, 1);
        this.$data.currentpage = Math.ceil(this.$data.tableData.length/this.$data.pagesize);
        this.getPageInfo();
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    handleEdit2(index, row) {
      row.isEdit = true;
      this.$data.oneEdit2 = true;
      this.$data.dialogTempNum = row.number;
      this.$data.forceRefresh = 'a';
    },
    handleSave2(index, row) {
      if(row.number == null || row.number == '') {
        this.$message.error("请输入盛放个数")
        return
      }
      else if(this.$data.dialogTempNum != row.number){
        row.isChanged = true;
      }
      row.isEdit = false;
      this.$data.oneEdit2 = false;
      this.$data.forceRefresh = 'b';
    },
    handleCreate(index, row) {
      row.isEdit2 = true;
      this.$data.dialogTempNum = row.often_number;
      this.$data.forceRefresh = 'a';
    },
    handleCreate2(index, row) {
      if(row.often_number == null || row.often_number == '') {
        
      }
      else{
        // 创建数据
        var obj = {
          rollThickness: row.item_hd,
          rollLength: row.item_cd,
          rollName: "普通卷膜",
          palletId: this.$data.form.tray_size,
          rollNums: row.often_number
        }
        create_palletroll(obj).then((res) => {
          row.isNull = false;
        }).catch((error) => {
          console.log(error)
          this.$message.error("创建失败")
        })
      }
      row.isEdit2 = false;
      this.$data.forceRefresh = 'b';
    },
    tray1111(row) {
      let showProp = null
      row.often_number ? showProp = row.often_number : showProp = '---'
      return showProp
    },
    // exitCheck(name, row) {
    //   row[name] = row[name]
    //                .replace(/[^\-\d.]/g, '')  //只能输入   数字 小数点 -
    //                .replace(/\-{2,}/g, "-") // 只能出现一次- 
    //                .replace(/^0+(\d)/, '$1') //如果第一位是 0 就替换成后面的数字
    //                .replace(/^\./, '0.') //如果第一位是 . 就 替换成  0.
    //                .match(/^[\d\-]*(\.?\d{0,5})/g)[0] || ''  //开头只能允许数字或者 -
    // },
    // exitSave(name, row) {
    //   row[name] = parseFloat(row[name])
    // },
    // 增加车箱项
    exitCheck(name, row) {
      row[name] = check(row[name])
    },
    exitSave(name, row) {
      row[name] = save(row[name])
    },
    exitCheck_density(num) {
      this.$data.form.default_density = check(num)
    },
    exitSave_density(num) {
      this.$data.form.default_density = save(num)
    },
    logicCheck() {
      const selectedVehicleHeights = this.$data.form.box_list
        .map(item => this.options_box_type.find(option => option.value == item.box_id))
        .filter(Boolean)
        .map(option => Number(option.height) * 100)
      const minVehicleHeightCm = selectedVehicleHeights.length ? Math.min(...selectedVehicleHeights) : null
      const overlapError = validateOverlapConfig(this.$data.form, minVehicleHeightCm)
      if (overlapError) {
        this.activeName = 'first'
        this.$message.error(overlapError)
        return false
      }
      return true;
    },
    removeBox2(index, row) {
      if (index !== -1) {
        this.$data.form.box_list.splice(index, 1)
      }
      // this.getBoxHeight();
    },
    addBox2() {
      this.$data.form.box_list.push({
        box_id: this.$data.box_id,
        num: 1,
        key: Date.now()
      });
      // this.getBoxHeight();
    },
    // 获取box_list中的最大高度
    getBoxHeight() {
      var max_height = 0;
      this.$data.form.box_list.forEach((item) => {
        var box_height = this.options_box_type.find(item2 => item2.value == item.box_id).height
        max_height = Math.max(max_height, box_height)
      })
      this.$data.box_max_height = max_height * 100; //转换为cm
    },
    //form动态禁止
    traySize() {
      if (this.$data.form.tray_rule == "human") {
        this.$data.show_tray = false
      } else {
        this.$data.show_tray = true
      }
    },
    overlap() {
      if (this.$data.form.overlap) {
        this.$data.input_overlap = false
      } else {
        this.$data.input_overlap = true
        this.$nextTick(() => {
          this.$refs.form.clearValidate(['single_max_height', 'entire_max_height'])
        })
      }
    },
    lying() {
      if (this.$data.form.lying) {
        this.$data.input_lying = false
      } else {
        this.$data.input_lying = true
        console.log(this.$data.form.lying_limit)
        if(this.$data.form.lying_limit == ""){
          this.$data.form.lying_limit = 4
        }
      }
    },
    //分页数据刷新
    getPageInfo() {
      //清空pageTicket中的数据
      this.$data.pageData = [];
      this.$data.total = this.$data.tableData.length
      if(this.$data.total == 0){
        this.$data.currentpage = 1;
        return;
      }
      // 获取当前页的数据
      for (let i = (this.$data.currentpage - 1) * this.$data.pagesize; i < this.$data.total; i++) {
        //把遍历的数据添加到pageTicket里面
        this.$data.pageData.push(this.$data.tableData[i]);
        //判断是否达到一页的要求
        if (this.$data.pageData.length === this.$data.pagesize) break;
      }
    },
    //分页时修改每页的行数,这里会自动传入一个size
    handleSizeChange(size) {
      //修改当前每页的数据行数
      this.$data.pagesize = size;
      //数据重新分页
      this.getPageInfo();
    },
    //调整当前的页码
    handleCurrentChange(pageNumber) {
      //修改当前的页码
      this.$data.currentpage = pageNumber;
      //数据重新分页
      this.getPageInfo()
    },
    // dialog控制
    handleClose() {
      this.$confirm('确认关闭？')
          .then(_ => {
            this.cancelDialog();
          })
          .catch(_ => {});
    },
    cancelDialog() {
      this.$data.loading = false;
      this.$data.loading2 = false;
      this.$data.dialogTableVisible = false;
    },
    async submitDialog() {
      // this.$data.dialogTableVisible = false;
      var data = {
        taskId: this.$data.taskId,
        data: this.$data.dialog
      }
      this.$data.loading2 = true;
      try {
        const res = await post_al_second(data)
        console.log(res)
      } catch (error) {
        this.$data.loading2 = false;
        console.log(error)
        this.$message.error("二阶段提交失败，请重新提交")
      }
    },
    web_socket() {
      const that = this
      if (typeof WebSocket === 'undefined') {
        this.$data.wsp = true
        this.$message.error('当前浏览器不支持 WebSocket')
        return
      }

      if (this.$data.ws && typeof this.$data.ws.close === 'function') {
        this.$data.ws.close()
      }
      this.$data.wsp = true

      const client = new ReconnectingWebSocket({
        url: () => buildWebSocketUrl('/palletpackingWebsocket', getToken()),
        onOpen: socket => {
          console.log('WebSocket connected')
          socket.send('from client: hello')
        },
        onStatusChange: connected => {
          that.$data.wsp = !connected
        },
        onReconnect: retryCount => {
          if (retryCount === 1) {
            that.$message({
              message: 'WebSocket 连接中断，正在自动重连…',
              type: 'warning',
              duration: 3000
            })
          }
        },
        onMessage: e => {
          let res
          try {
            res = JSON.parse(e.data)
          } catch (error) {
            console.error('WebSocket 消息解析失败', error, e.data)
            return
          }
        // 这里要做一个code的判断 一阶段
        if (res.code == 10001 && res.data.taskId == that.$data.taskId) {
          var data = JSON.parse(res.data.result);
          that.$data.dialog = data;
          that.$data.dialog.forEach((res) => {
            Object.assign(res, { isEdit: false, isEdit2: false, isChanged: false, isNull: false });
            if(res.often_number==null){
              res.isNull = true;
            }
          })
          that.$data.dialogTableVisible = true;
        } else if(res.code == 10002 && res.data.taskId == that.$data.taskId) {
          that.$data.loading = false;
          that.$data.loading2 = false;
          that.$data.dialogTableVisible = false;
          var obj = JSON.parse(res.data.result);
          var taskId = res.data.taskId;
          var config = that.$data.form;
          console.log(obj)
          // console.log(arr)
          that.$router.push({
            path: '/type1/3D_result',
            query: {
              obj: JSON.stringify(obj),
              taskId: JSON.stringify(taskId),
              config: JSON.stringify(config)
            }
          }) // 带参跳转
        } else if(res.code != 10001 && res.code != 10002) {
          that.$message({
            message: res.message+"wb",
            type: 'error',
            duration: 5 * 1000
          })
          that.$data.loading = false;
          that.$data.loading2 = false;
          that.$data.dialogTableVisible = false;
        }
        }
      })

      this.$data.ws = client
      client.connect()
    }
  },
  created() {
    this.init()
    // if ("source" in this.$route.query && this.$route.query.source.config != null){
    //   // console.log("to_route")
    //   // console.log(this.$route.query)
    //   this.$data.form = this.$route.query.source.config
    //   this.$data.tableData = this.$route.query.source.tableData
    //   this.getPageInfo()
    // }
  },
  mounted() {
    this.web_socket()
  },
  beforeDestroy() {
    if (this.$data.ws && typeof this.$data.ws.close === 'function') {
      this.$data.ws.close()
    }
  },
  activated(){
    if ("source" in this.$route.query && this.$route.query.source.config != null){
          this.$data.form = this.$route.query.source.config
          this.$data.tableData = this.$route.query.source.tableData
          this.getPageInfo()
        }
  },
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.el-tabs--card {
  // height: calc(100vh - 110px);
  height: 800px;
  /* overflow-y: auto; */
}

.el-tab-pane {
  height: 800px;
  overflow-y: auto;
}

.overlap-rule-tip {
  width: calc(100% - 40px);
  margin: 0 20px 20px;
}

.height-conversion-tip {
  margin-left: 8px;
  color: #606266;
  white-space: nowrap;
}

.data-import-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  padding-right: 20px;
}

// .el-form-item {
//   height: 30px;
// }</style>
<style lang="scss">
.title .el-form-item__label {
  font-size: 30px;
}

.title .el-form-item {
  margin-bottom: 30px;
  border-bottom-width: none;
}

.el-form-item {
  margin-bottom: 30px;
}
.three .el-form-item{
  margin-bottom: 0px;
}
</style>
