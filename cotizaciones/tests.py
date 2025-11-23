from django.test import TestCase

from cotizaciones.templatetags.phone_filters import phone_whatsapp
from cotizaciones.templatetags.file_filters import basename


class TemplateTagTests(TestCase):
	def test_phone_whatsapp_various_formats(self):
		self.assertEqual(phone_whatsapp('+56 9 1234 5678'), '56912345678')
		self.assertEqual(phone_whatsapp('56 9 1234 5678'), '56912345678')
		self.assertEqual(phone_whatsapp('9 1234 5678'), '56912345678')
		self.assertEqual(phone_whatsapp('00912345678'), '56912345678')
		self.assertEqual(phone_whatsapp(''), '')

	def test_basename_filter(self):
		self.assertEqual(basename('uploads/docs/presupuesto_1.pdf'), 'presupuesto_1.pdf')

		class FakeField:
			name = 'folder/sub/doc.docx'

		fake = FakeField()
		self.assertEqual(basename(fake), 'doc.docx')
