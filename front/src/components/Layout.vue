<template>
  <el-container class="layout-container">
    <!-- 顶部标题栏 -->
    <el-header class="header">
      <!-- 标题容器 -->
      <div class="title-container">
        <h1 class="system-title">涅槃</h1>
        <div class="divider"></div>
        <h2 class="system-subtitle">入侵检测系统</h2>
      </div>
    </el-header>
    <!-- 主体内容区域 -->
    <el-container>
      <!-- 左侧导航菜单 -->
      <el-aside width="200px">
        <el-menu
          :default-active="activeIndex"
          class="menu"
          @select="handleSelect"
        >
          <!-- 实时监测功能菜单组 -->
          <el-sub-menu index="1">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>实时监测功能</span>
            </template>
            <el-menu-item index="/overview">概览</el-menu-item>
            <el-menu-item index="/details">详细信息</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      <!-- 右侧主内容区域 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Monitor } from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: {
    Monitor
  },
  setup() {
    // 路由实例
    const router = useRouter()
    // 当前激活的菜单项
    const activeIndex = ref('/overview')

    // 处理菜单选择事件
    const handleSelect = (index) => {
      router.push(index)
    }

    return {
      activeIndex,
      handleSelect
    }
  }
}
</script>

<style scoped>
/* 布局容器样式 */
.layout-container {
  height: 100vh;
}

/* 顶部标题栏样式 */
.header {
  background: linear-gradient(90deg, #409EFF, #2c5cff);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 标题容器样式 */
.title-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 主标题样式 */
.system-title {
  font-size: 28px;
  font-weight: bold;
  letter-spacing: 2px;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

/* 分隔线样式 */
.divider {
  height: 24px;
  width: 2px;
  background-color: rgba(255, 255, 255, 0.6);
  margin: 0 5px;
}

/* 副标题样式 */
.system-subtitle {
  font-size: 20px;
  font-weight: normal;
  margin: 0;
  opacity: 0.9;
}

/* 菜单样式 */
.menu {
  height: 100%;
}
</style> 