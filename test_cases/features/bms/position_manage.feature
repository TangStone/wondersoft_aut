# Created by gaojie at 2024-04-22
Feature: 职位管理模块
  用户管理 -> 基础数据管理 -> 职位管理模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：基础数据管理 下的三级菜单：职位管理

  Scenario: 导入职位-模板内填写全部信息
    Given 点击按钮：导入职位
    When 点击按钮：模板下载
    Then 弹出提示框，显示提示信息：下载成功
    When 上传职位文件：职位导入.xlsx
    Then 弹出提示框，显示提示信息：导入成功
    When 点击按钮：搜索
    Then 职位列表中包含：研发、测试

  Scenario: 职位列表查询
    When 根据查询条件进行职位列表查询：
      """
        {
          "职位": "普通职员"
        }
      """

  Scenario Outline: 删除职位
    When 删除职位：<职位>
    Examples:
      | 职位  |
      | 研发    |
      | 测试    |