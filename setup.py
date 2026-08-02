import os
import sys
import shutil
import json
from pathlib import Path

def setup_skills():
    print("🚀 正在为您自动安装并配置 Agent 技能库...")
    
    # 1. 确定目标 Skill 安装路径
    user_home = Path.home()
    global_skills_dir = user_home / ".gemini" / "config" / "skills"
    global_skills_dir.mkdir(parents=True, exist_ok=True)
    
    current_dir = Path(__file__).parent.resolve()
    source_skills_dir = current_dir / "skills"
    
    if not source_skills_dir.exists():
        print("❌ 未能找到 skills 目录！")
        sys.exit(1)
        
    manifest_file = current_dir / "SKILL_MANIFEST.json"
    skills_to_install = []
    
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            skills_to_install = [s["name"] for s in manifest.get("skills", [])]
    else:
        skills_to_install = [d.name for d in source_skills_dir.iterdir() if d.is_dir()]
        
    installed_count = 0
    for skill_name in skills_to_install:
        src = source_skills_dir / skill_name
        dest = global_skills_dir / skill_name
        
        if src.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            print(f"  ✅ 已成功挂载 Skill: {skill_name} -> {dest}")
            installed_count += 1
            
    print(f"\n🎉 全部完成！已为您成功装载 {installed_count} 个 Skill 到系统全局配置中。")
    print("现在所有的 Agent (Antigravity 等) 均已支持并可直接调用这些 Skill！")

if __name__ == "__main__":
    setup_skills()
