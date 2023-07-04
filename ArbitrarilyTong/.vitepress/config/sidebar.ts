import { DefaultTheme } from "vitepress";

const sidebarConfig: DefaultTheme.Sidebar = {
  "/About/": [
    {
      text: "关于",
      items: [
        { text: "项目介绍", link: "/About/" },
        { text: "团队成员", link: "/About/TeamMates" },
      ],
    },
  ],
  "/FAQ/": [
    {
      text: "常见问题",
      items: [
        { text: "简介", link: "/FAQ/" },
        { text:"加入我们", link:"/FAQ/JoinUs" }
    ],
    },
  ],
  "/Guide/": [
    {
      text: "开发指南",
      items: [
        { text: "前言", link: "/Guide/" },
        { text: "REPO 使用指北", link: "/Guide/how-to-fuck-up-repo"}
      ],
    },
  ],
};

export default sidebarConfig;
