<template>
  <div class="overview-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>HTTP流量分析</span>
            </div>
          </template>
          <div ref="tcpChartRef" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>攻击类型分布</span>
            </div>
          </template>
          <div ref="attackChartRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

export default {
  name: 'Overview',
  setup() {
    const tcpChartRef = ref(null)
    const attackChartRef = ref(null)
    let tcpChart = null
    let attackChart = null

    // 获取HTTP流量数据
    const fetchTcpData = async () => {
      try {
        const response = await fetch('http://43.128.112.182:4000/netlog/overview')
        const data = await response.json()
        
        // 更新HTTP流量图表
        tcpChart.setOption({
          series: [{
            data: [
              { value: data.evilPercent, name: '恶意HTTP请求' },
              { value: data.other, name: '正常请求' }
            ]
          }]
        })
      } catch (error) {
        console.error('获取HTTP流量数据失败:', error)
        ElMessage.error('获取HTTP流量数据失败')
      }
    }

    // 初始化HTTP流量图表
    const initTcpChart = () => {
      if (tcpChartRef.value) {
        tcpChart = echarts.init(tcpChartRef.value)
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {d}%'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              label: {
                show: true,
                formatter: '{b}: {d}%'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '16',
                  fontWeight: 'bold'
                }
              },
              data: [
                { value: 0, name: 'HTTP请求' },
                { value: 0, name: '其他请求' }
              ]
            }
          ]
        }
        tcpChart.setOption(option)
      }
    }

    // 获取攻击类型数据
    const fetchAttackData = async () => {
      try {
        const response = await fetch('http://43.128.112.182:4000/attlog/overview')
        const data = await response.json()
        
        // 更新攻击类型图表
        attackChart.setOption({
          series: [{
            data: data.map(item => ({
              name: item.class,
              value: item.percent
            }))
          }]
        })
      } catch (error) {
        console.error('获取攻击类型数据失败:', error)
        ElMessage.error('获取攻击类型数据失败')
      }
    }

    // 初始化攻击类型图表
    const initAttackChart = () => {
      if (attackChartRef.value) {
        attackChart = echarts.init(attackChartRef.value)
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {d}%'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            padding: [20, 0, 0, 0]
          },
          series: [
            {
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              label: {
                show: true,
                formatter: '{b}\n{d}%'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '16',
                  fontWeight: 'bold'
                }
              },
              data: []
            }
          ]
        }
        attackChart.setOption(option)
      }
    }

    // 处理窗口大小变化
    const handleResize = () => {
      tcpChart?.resize()
      attackChart?.resize()
    }

    onMounted(() => {
      initTcpChart()
      initAttackChart()
      fetchTcpData()
      fetchAttackData()
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      tcpChart?.dispose()
      attackChart?.dispose()
      window.removeEventListener('resize', handleResize)
    })

    return {
      tcpChartRef,
      attackChartRef
    }
  }
}
</script>

<style scoped>
.overview-container {
  padding: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.chart {
  height: calc(100vh - 400px);
  min-height: 300px;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  background-color: #f5f7fa;
}
</style> 