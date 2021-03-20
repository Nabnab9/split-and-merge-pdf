pdf-toyota-latest:
  git.latest:
    - name: git@github.com:Nabnab9/split-and-merge-pdf.git
    - target: /opt/split-and-merge-pdf
    - identity: /home/banban/.ssh/id_rsa

requirements-installed:
  pip.installed:
    - requirements: /opt/split-and-merge-pdf/requirements.txt

systemd service pdf-toyota:
  file.managed:
    - name: /etc/systemd/system/pdf.service
    - source: /srv/salt/pdf.service
    - user: root
    - group: root
    - mode: 755
  service.running:
    - name: pdf.service
    - enable: True

vhost pdf toyota:
  file.managed:
    - name: /etc/httpd/conf.d/pdf.nabnab.fr.conf
    - source: /srv/salt/pdf.nabnab.fr.conf
    - user: root
    - group: root
    - mode: 644
