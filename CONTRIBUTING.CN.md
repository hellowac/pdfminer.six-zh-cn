# 贡献指南  

任何贡献都受到欢迎！你可以：  

- 修正拼写错误  
- 改进文档  
- 为尚未测试的代码添加测试  
- 添加新功能  
- 修复错误  

## 我该如何贡献？  

- 使用 [issues](https://github.com/pdfminer/pdfminer.six/issues) 来报告错误和建议新功能  
    - 如果你报告的是某个 PDF 解析结果的错误，请附上该 PDF 文件，以便其他人能够复现问题。  
- 通过 [创建 Pull Request](https://help.github.com/en/articles/creating-a-pull-request) 来修复问题。  
- 在 issue 和 pull request 的评论区分享你的想法，帮助他人。  
- 加入 [Gitter 聊天室](https://gitter.im/pdfminer-six/Lobby)。  

## 提交 issue 的指南  

- 在提交 issue 之前，先搜索已有的 issue，避免重复提交。  
- 如果是错误报告，请提供一个最小可复现示例。  
- 如果是功能请求，请描述你希望解决的问题的背景，以便其他人理解该功能的价值。  

## 提交 Pull Request 的指南  

- Pull Request 应该与现有 issue 相关。例如，使用 "Fix #123" 来表明你的 PR 修复了 issue #123。  
- Pull Request 应该合并到 `master` 分支。  
- 尽可能包含单元测试。如果是 bug 修复，测试可以防止未来出现相同的错误。如果是新功能，测试可以验证代码是否正确。  
- 代码应兼容 Python 3.8 及以上版本。  
- 使用 `nox` 运行测试（见下文）。  
- 新功能应通过 docstring 进行充分的文档化。  
- 检查是否需要更新 [README.md](../README.md) 或 [ReadTheDocs](../docs/source) 文档。  
- 检查拼写和语法错误。  
- 记得更新 [CHANGELOG.md](CHANGELOG.md#[Unreleased])。  

## 评论指南  

- [保持友好和积极](https://kennethreitz.org/essays/2013/01/27/be-cordial-or-be-on-your-way)。  

## 发布指南  

- 发布流程已自动化。添加 YYYYMMDD 格式的版本标签，GitHub workflows 会自动完成发布。  

## 依赖管理指南  

- 本项目采用 [MIT 许可证](LICENSE)。  
- 所有依赖项都应与该许可证兼容。  
- 使用 [licensecheck](https://pypi.org/project/licensecheck/) 来验证新依赖项的兼容性。  

## 开始使用  

1. 克隆存储库  

  ```sh
  git clone https://github.com/pdfminer/pdfminer.six
  cd pdfminer.six
  ```

2. 安装开发依赖  

  ```sh
  pip install -e ".[dev]"
  ```

3. 运行格式化、代码检查和测试  

  在所有 Python 版本上运行：  

  ```sh
  nox
  ```

  或者仅在特定 Python 版本（如 3.12）上运行测试：  

  ```sh
  nox -e tests-3.12
  ```
