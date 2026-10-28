import flet as ft
import json
import os

DATA_FILE = "../tasks.json"

def load_tasks():
    """从文件读取任务列表"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """把任务列表写入文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def main(page: ft.Page):
    page.title = "Odd Town"
    page.padding = 20

    tasks = load_tasks()  # 启动时加载

    task_input = ft.TextField(
        hint_text="输入待办事项，按enter或click-添加-",
        expand=True,
        on_submit=lambda e: add_task(e),
    )
    task_list = ft.Column(spacing=8)

    def refresh_tasks():
        """根据 tasks 列表重新渲染界面"""
        task_list.controls.clear()
        for i, text in enumerate(tasks):
            row = ft.Row(
                controls=[
                    ft.Text(text, expand=True, size=16),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_400,
                        on_click=lambda e, idx=i: delete_task(idx),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            task_list.controls.append(row)

    def add_task(e):
        text = task_input.value.strip()
        if not text:
            return
        tasks.append(text)
        save_tasks(tasks)      # 每次修改后保存
        task_input.value = ""
        refresh_tasks()
        page.update()

    def delete_task(idx):
        tasks.pop(idx)
        save_tasks(tasks)      # 每次修改后保存
        refresh_tasks()
        page.update()

    page.add(
        ft.Row(
            controls=[task_input, ft.Button(content="添加", on_click=add_task)],
            spacing=10,
        ),
        ft.Divider(),
        task_list,
    )
    refresh_tasks()  # 启动时把已存的任务显示出来

# 兼容不同版本的 Flet 启动方式
#if hasattr(ft, "run"):
#    ft.run(main)
#else:
#    ft.app(main)

#new version
ft.run(main)