import magic

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

# TODO: 複数ファイルっプロード時にすべてのファイルに対してvalidation実行
# TODO: ファイルサイズと拡張子のvalidationerrorを同時に表示

@deconstructible
class FileValidator:
    error_messages = {
        'max_size': 'ファイルサイズが%(max_size)s以下に'\
        'なるようにしてください。アップロードされたファイル'\
        'のサイズは%(size)sです。',
        'content_type': '%(content_type)sはサポートされていません'
    }

    def __init__(self, max_size=None, content_types=()):
        self.max_size = max_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                    'max_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                        'content_type', params)

    def __eq__(self, other):
        return (
            isinstance(other, Filevalidator) and
            self.max_size == other.max_size and
            self.content_types == other.content_types
        )
