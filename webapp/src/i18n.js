import { createI18n } from 'vue-i18n'
import en from './locales/en'

const i18n = createI18n({
  legacy: false, // Set to false to use Composition API
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en }
})

export default i18n