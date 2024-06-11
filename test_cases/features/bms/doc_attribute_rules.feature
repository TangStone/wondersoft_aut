# Created by gaojie at 2024-04-28
Feature: 文件属性规则
  规则管理 -> 文件属性规则 -> 文件属性规则 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：规则管理
    And 进入二级菜单：文件属性规则 下的三级菜单：文件属性规则

  Scenario: 新增文件类型属性规则
    Given 点击按钮：新增属性规则
    When 输入新增属性规则信息：
      """
        {
          "规则名称": "exe类型规则",
          "规则类型": "文件类型",
          "文件分类": ["文件分类根目录->可执行文件格式"],
          "识别类型": {
            "格式识别类型": {
              "可执行文件格式": ["exe"]
            }
          }
        }
      """
    When 点击【新增属性规则】页面的【确定】按钮
    Then 弹出提示框，显示提示信息：新增成功

  Scenario: 文件属性规则查询
    When 根据查询条件进行文件属性规则查询：
      """
        {
          "属性类型": "文件类型"
        }
      """

  Scenario Outline: 删除文件属性规则
    When 删除文件属性规则：<文件属性规则名称>
    Examples:
      | 文件属性规则名称  |
      | exe类型规则      |