def validate_not_empty(value):
    # Проверка "а заполнено ли поле?"
    if value == '':
        raise forms.ValidationError(
            'Это поле обязательно для заполнения',
            params={'value': value},
        )
