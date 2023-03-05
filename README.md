# gurad 簡單資源監控
監控 yaml 檔案所設定的項目，目前監控的項目
- folder
  - folder_size:  特定資料夾的大小

## 基本設定範本
```yaml
monitor:
  項目一:
    項目相關設定
  項目二：
    項目相關設定
Log:
  dir: [PATH/TO/FOLDER]
  file: [LOG/FILE/NAME]
```

## folder
### metric: folder_size
  - 設定方法
    ``` yaml
    monitor:
      folder:
        size:
          - /tmp
          - /var/log
    ```


