# -*- coding: utf-8 -*-i

from djmail import template_mail


class NotificationSenderMixin(object):
    create_notification_template = None
    update_notification_template = None
    destroy_notification_template = None

    def _send_notification_email(template_method, users=None, context=None):
        mails = template_mail.MagicMailBuilder()
        for user in users:
            email = getattr(mails, template_method)(user, context)
            email.send()

    def post_save(self, obj, created=False):
        users = obj.get_watchers_to_notify(self.request.user)
        context = {
            'changer': self.request.user,
            'changed_fields_dict': obj.get_changed_fields_dict(self.request.DATA),
            'object': obj
        }

        if created:
            #self._send_notification_email(self.create_notification_template, users=users, context=context)
            print "TODO: Send the notification email of object creation"
        else:
            #self._send_notification_email(self.update_notification_template, users=users, context=context)
            print "TODO: Send the notification email of object modification"

    def destroy(self, request, *args, **kwargs):
        users = obj.get_watchers_to_notify(self.request.user)
        context = {
            'changer': self.request.user,
            'object': obj
        }
        #self._send_notification_email(self.destroy_notification_template, users=users, context=context)
        print "TODO: Send the notification email of object deletion"

        return super(NotificationSenderMixin, self).destroy(request, *args, **kwargs)
