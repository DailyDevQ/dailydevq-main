import Link from "next/link";
import { Button } from "@/components/ui/button";
import LanguageToggle from "./language-toggle";

interface HeaderProps {
  t: {
    features: string;
    login: string;
    subscribe: string;
  };
  language: "en" | "ko";
  toggleLanguage: (lang: "en" | "ko") => void;
}

export default function Header({ t, language, toggleLanguage }: HeaderProps) {
  return (
    <header className="px-4 lg:px-6 h-14 flex items-center border-b">
      <Link href="/" className="flex items-center justify-center">
        <span className="font-bold text-2xl">DailyDevQ</span>
      </Link>
      <nav className="ml-auto flex items-center gap-4 sm:gap-6">
        <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
          {t.features}
        </a>
        <LanguageToggle language={language} toggleLanguage={toggleLanguage} />
        <Link href="/login">
          {/* variant 속성 사용 */}
          <Button variant="outline" className="hidden sm:inline-flex">
            {t.login}
          </Button>
        </Link>
        <Link href="/login">
          {/* variant 속성 사용 */}
          <Button variant="default" className="hidden sm:inline-flex bg-purple-600 text-white">
            {t.subscribe}
          </Button>
        </Link>
      </nav>
    </header>
  );
}
