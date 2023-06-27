# 项目介绍

你好，世界！

ArbitrarilyTong<Badge type="info">任意桐</Badge> 是一个基于 `crDroid` 的类原生 Android ROM。

<script setup>
  import { theme } from 'ant-design-vue';import { useData } from 'vitepress'

const { isDark } = useData()
</script>
<a-config-provider
    :theme="{
      algorithm: isDark ? theme.darkAlgorithm : theme.defaultAlgorithm,
    }"
>   
<a-divider orientation="left">开发进度</a-divider>
<a-timeline>
    <a-timeline-item>
        正式立项，后由Respect OWl加入并协助设计工作 2023-02-26
    </a-timeline-item>
    <a-timeline-item color="green">
        ArbitrarilyTong放出第一个测试包 2023-03-25
    </a-timeline-item>
    <a-timeline-item color="red">
        开始转移至LineageOS作为系统底层 2023-05-28
    </a-timeline-item>
    <a-timeline-item>
      开始转移至crDroid作为系统底层 2023-06-23
    </a-timeline-item>
</a-timeline>
</a-config-provider>

![](https://arbitrarilytong.win/img/moegirlbanner.png)
