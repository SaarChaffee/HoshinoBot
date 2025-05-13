import subprocess
import re
import os
import yaml

def clean_package_name(package_spec):
    """提取纯包名（移除版本信息和额外选项）"""
    # 处理[extras]情况
    if '[' in package_spec:
        base_name = package_spec.split('[')[0]
        extra = package_spec.split('[')[1].split(']')[0] if ']' in package_spec else ''
        package_spec = base_name  # 暂时只保留基础包名用于检查
    
    # 移除版本号
    package = re.split(r'[=~<>!]', package_spec)[0].strip()
    return package

def get_version_spec(package_line):
    """提取版本限定符"""
    if '==' in package_line:
        return '=='
    elif '~=' in package_line:
        return '~='
    elif '>=' in package_line:
        return '>='
    elif '<=' in package_line:
        return '<='
    elif '>' in package_line:
        return '>'
    elif '<' in package_line:
        return '<'
    elif '!=' in package_line:
        return '!='
    return None

def get_version_requirement(package_line):
    """提取版本号要求"""
    for spec in ['==', '~=', '>=', '<=', '>', '<', '!=']:
        if spec in package_line:
            return package_line.split(spec)[1].strip()
    return None

def check_conda_availability(package_name):
    """检查包是否在conda中可用"""
    try:
        result = subprocess.run(
            ['conda', 'search', '--quiet', package_name],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False

def get_conda_version(package_name, version_requirement=None, version_spec=None):
    """获取conda仓库中的版本号"""
    try:
        result = subprocess.run(
            ['conda', 'search', package_name],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            return None
            
        lines = result.stdout.strip().split('\n')
        if len(lines) <= 2:  # 标题行和分隔行
            return None
            
        # 解析版本信息
        versions = []
        for line in lines[2:]:  # 跳过标题行和分隔行
            parts = line.split()
            if len(parts) >= 2:
                versions.append(parts[1])  # 版本号通常在第二列
        
        if not versions:
            return None
            

        # 如果有版本要求，尝试匹配
        if version_requirement and version_spec:
            # 简单实现：对于~=和==，尝试找到匹配的版本
            if version_spec in ('~=', '=='):
                if version_requirement in versions:
                    return version_requirement
                # 对于~=，尝试找到兼容版本
                if version_spec == '~=':
                    base_version = '.'.join(version_requirement.split('.')[:2])
                    for v in sorted(versions, reverse=True):
                        if v.startswith(base_version):
                            return v
            
        # 如果没有匹配，返回最新版本
        return sorted(versions, key=lambda x: [int(n) for n in x.split('.')])[-1]
    except Exception as e:
        print(f"获取{package_name}的conda版本时出错: {e}")
        return None

def convert_requirements_to_conda(requirements_file, output_file="environment.yml"):
    """转换requirements.txt到conda环境文件"""
    # 读取requirements.txt
    with open(requirements_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('//')]
    
    # 初始化环境文件结构
    env_dict = {
        'name': 'hoshino',
        'channels': ['conda-forge', 'anaconda'],
        'dependencies': ['python=3.8']
    }
    
    pip_dependencies = []
    
    print("检查包在conda中的可用性...")
    
    for line in lines:
        original_line = line
        package = clean_package_name(line)
        version_spec = get_version_spec(line)
        version_req = get_version_requirement(line)
        
        # 检查包是否可在conda中安装
        if check_conda_availability(package):
            conda_version = get_conda_version(package, version_req, version_spec)
            if conda_version:
                env_dict['dependencies'].append(f"{package}={conda_version}")
                print(f"✓ {package}: 使用conda版本 {conda_version}")
            else:
                env_dict['dependencies'].append(package)
                print(f"✓ {package}: 使用conda最新版本")
        else:
            pip_dependencies.append(original_line)
            print(f"⨯ {package}: 仅通过pip安装")
    
    # 如果有pip依赖，添加pip部分
    if pip_dependencies:
        env_dict['dependencies'].append({'pip': pip_dependencies})
    
    # 写入环境文件
    with open(output_file, 'w') as f:
        yaml.dump(env_dict, f, default_flow_style=False, sort_keys=False)
    
    print(f"\n成功生成环境文件: {output_file}")
    print(f"共处理 {len(lines)} 个包，其中 {len(lines) - len(pip_dependencies)} 个可通过conda安装")

if __name__ == "__main__":
    # 确保PyYAML已安装
    try:
        import yaml
    except ImportError:
        print("需要安装PyYAML。正在安装...")
        subprocess.run(['pip', 'install', 'pyyaml'], check=True)
        import yaml
        
    convert_requirements_to_conda("requirements.txt")