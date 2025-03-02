import { Button } from "@/components/ui/button"

export default function LanguageToggle({ language, toggleLanguage }) {
  return (
    <Button onClick={toggleLanguage} variant="ghost" size="icon">
      {language === "kr" ? "🇰🇷" : "🇺🇸"}
    </Button>
  )
}

