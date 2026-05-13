import argparse
import sys
import os
from qassemrpm.builder import build_spec

def main():
    # 1. إعداد المعالج الأساسي
    parser = argparse.ArgumentParser(
        description="QassemRPM: A modern RPM packaging tool for developers."
    )
    
    # 2. إضافة الأوامر الفرعية (Sub-commands)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # إعداد أمر البناء (build)
    build_parser = subparsers.add_parser("build", help="Build an RPM from a SPEC file")
    build_parser.add_argument("spec", help="Path to the .spec file (e.g., examples/hello.spec)")
    build_parser.add_argument("--workdir", help="Custom workspace directory (_topdir)", default=None)

    args = parser.parse_args()

    # 3. معالجة أمر build
    if args.command == "build":
        # التحقق من وجود ملف الـ SPEC قبل البدء
        if not os.path.exists(args.spec):
            print(f"\033[91m❌ Error: File '{args.spec}' not found.\033[0m")
            sys.exit(1)

        print(f"\033[94m🛠️  Building RPM for: {args.spec}...\033[0m")
        
        # استدعاء المحرك
        success, output = build_spec(args.spec, topdir=args.workdir)
        
        if success:
            print("\033[92m✅ Build completed successfully!\033[0m")
            print("\033[90m" + "-"*30 + " LOGS " + "-"*30 + "\033[0m")
            print(output)
        else:
            print("\033[91m🛑 Build failed! Check the logs below:\033[0m")
            print("\033[90m" + "-"*30 + " ERROR " + "-"*30 + "\033[0m")
            print(output)
            sys.exit(1)
    else:
        # عرض المساعدة إذا لم يتم إدخال أمر
        parser.print_help()

if __name__ == "__main__":
    main()
