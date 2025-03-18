<template>
  <div class="details-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="table-card">
          <template #header>
            <div class="card-header">
              <span>所有TCP流量显示</span>
            </div>
          </template>
          <el-table
            :data="tcpData"
            height="calc(100vh - 320px)"
            style="width: 100%"
            v-loading="loading"
            border
            stripe
          >
            <el-table-column prop="timestamp" label="时间" width="180" align="center" />
            <el-table-column prop="sourceIp" label="源IP" width="140" align="center" />
            <el-table-column prop="destIp" label="目的IP" width="140" align="center" />
            <el-table-column prop="attackType" label="信息" min-width="120" align="center" />
            <el-table-column prop="httpPayload" label="HTTP报文" width="120" align="center">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click="showHttpPayload(scope.row)"
                >
                  查看报文
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="tcpCurrentPage"
              :page-size="10"
              :pager-count="5"
              layout="prev, pager, next, total"
              :total="tcpTotal"
              background
              @current-change="handleTcpCurrentChange"
            />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="table-card">
          <template #header>
            <div class="card-header">
              <span>报警流量显示</span>
              <el-select
                v-model="selectedAttackClass"
                placeholder="选择攻击类型"
                clearable
                @change="handleAttackClassChange"
                class="attack-type-select"
              >
                <el-option
                  v-for="item in attackClasses"
                  :key="item"
                  :label="item"
                  :value="item"
                />
              </el-select>
            </div>
          </template>
          <el-table
            :data="alertData"
            height="calc(100vh - 320px)"
            style="width: 100%"
            v-loading="loading"
            border
            stripe
          >
            <el-table-column prop="timestamp" label="时间" width="180" align="center" />
            <el-table-column prop="sourceIp" label="源IP" width="140" align="center" />
            <el-table-column prop="destIp" label="目的IP" width="140" align="center" />
            <el-table-column prop="attackType" label="信息" min-width="120" align="center" />
            <el-table-column prop="httpPayload" label="HTTP报文" width="120" align="center">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click="showHttpPayload(scope.row)"
                >
                  查看报文
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="alertCurrentPage"
              :page-size="10"
              :pager-count="5"
              layout="prev, pager, next, total"
              :total="alertTotal"
              background
              @current-change="handleAlertCurrentChange"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- HTTP报文对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="HTTP报文详情"
      width="60%"
      :before-close="handleClose"
    >
      <pre class="http-payload">{{ currentHttpPayload }}</pre>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Details',
  setup() {
    const loading = ref(false)
    const tcpData = ref([])
    const alertData = ref([])
    const dialogVisible = ref(false)
    const currentHttpPayload = ref('')

    // 分页相关的响应式变量
    const tcpCurrentPage = ref(1)
    const alertCurrentPage = ref(1)

    // 添加总数的响应式变量
    const tcpTotal = ref(0)
    const alertTotal = ref(0)

    // 添加攻击类型相关的变量
    const selectedAttackClass = ref('')
    const attackClasses = [
      'SQL注入攻击',
      'XSS注入攻击',
      '文件上传攻击',
      '命令执行攻击',
      '目录遍历攻击'
    ]

    // Base64解码方法
    const decodeBase64 = (base64String) => {
      if (!base64String) return '无HTTP报文数据'
      try {
        const decoded = atob(base64String)
        return decoded
      } catch (error) {
        console.error('Base64解码失败:', error)
        return '解码失败'
      }
    }

    // 添加时间格式化方法
    const formatTimestamp = (timestamp) => {
      if (!timestamp) return ''
      return timestamp.replace('-', ' ').split('.')[0]
    }

    // 获取TCP流量数据的方法
    const fetchTcpData = async () => {
      loading.value = true
      try {
        const response = await fetch(
          `http://43.128.112.182:4000/netlog?page=${tcpCurrentPage.value}&limit=10`
        )
        const { data, total } = await response.json()
        
        tcpTotal.value = total
        
        tcpData.value = (data || []).map(item => ({
          timestamp: formatTimestamp(item.timestamp),
          sourceIp: item.src_ap,
          destIp: item.dst_ap,
          attackType: item.msg,
          httpPayload: item.b64_data,
          rawData: item
        }))
      } catch (error) {
        console.error('获取TCP数据失败:', error)
        ElMessage.error('获取数据失败，请稍后重试')
        tcpData.value = []
        tcpTotal.value = 0
      }
      loading.value = false
    }

    // TCP流量分页处理
    const handleTcpCurrentChange = (val) => {
      tcpCurrentPage.value = val
      fetchTcpData()
    }

    // 获取告警流量数据的方法
    const fetchAlertData = async () => {
      loading.value = true
      try {
        const params = new URLSearchParams({
          page: alertCurrentPage.value.toString(),
          limit: '10'
        })
        
        // 如果选择了攻击类型，添加到参数中
        if (selectedAttackClass.value) {
          params.append('class', selectedAttackClass.value)
        }

        const response = await fetch(
          `http://43.128.112.182:4000/attlog/type?${params.toString()}`
        )
        const { data, total } = await response.json()
        
        alertTotal.value = total
        
        alertData.value = (data || []).map(item => ({
          timestamp: formatTimestamp(item.timestamp),
          sourceIp: item.src_ap,
          destIp: item.dst_ap,
          attackType: item.msg,
          httpPayload: item.b64_data,
          rawData: item
        }))
      } catch (error) {
        console.error('获取告警数据失败:', error)
        ElMessage.error('获取告警数据失败，请稍后重试')
        alertData.value = []
        alertTotal.value = 0
      }
      loading.value = false
    }

    // 告警流量分页处理
    const handleAlertCurrentChange = (val) => {
      alertCurrentPage.value = val
      fetchAlertData()
    }

    // 显示HTTP报文详情
    const showHttpPayload = (row) => {
      currentHttpPayload.value = decodeBase64(row.httpPayload)
      dialogVisible.value = true
    }

    // 处理对话框关闭
    const handleClose = () => {
      dialogVisible.value = false
    }

    // 处理攻击类型变化
    const handleAttackClassChange = () => {
      alertCurrentPage.value = 1  // 重置页码
      fetchAlertData()
    }

    onMounted(() => {
      fetchTcpData()
      fetchAlertData()
    })

    return {
      loading,
      tcpData,
      alertData,
      dialogVisible,
      currentHttpPayload,
      showHttpPayload,
      handleClose,
      // 分页相关
      tcpCurrentPage,
      alertCurrentPage,
      handleTcpCurrentChange,
      handleAlertCurrentChange,
      tcpTotal,
      alertTotal,
      selectedAttackClass,
      attackClasses,
      handleAttackClassChange,
    }
  }
}
</script>

<style scoped>
.details-container {
  padding: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.http-payload {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.dialog-footer {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  padding: 10px 0;
}

:deep(.el-pagination) {
  padding: 0;
  margin: 0;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #409EFF;
}

:deep(.el-pagination.is-background .el-pager li) {
  margin: 0 4px;
}

:deep(.el-table) {
  margin-top: 10px;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
  color: #606266;
  font-weight: bold;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: #fafafa;
}

:deep(.el-button--small) {
  padding: 6px 12px;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  background-color: #f5f7fa;
}

.attack-type-select {
  width: 160px;
}

/* 调整下拉框在卡片头部的样式 */
:deep(.el-select .el-input__wrapper) {
  background-color: white;
}

:deep(.el-select) {
  margin-left: 16px;
}
</style> 